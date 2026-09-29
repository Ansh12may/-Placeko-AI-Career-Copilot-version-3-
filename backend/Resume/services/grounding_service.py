
import json
import re
from typing import Dict, List, Tuple
from langchain_core.messages import HumanMessage, SystemMessage
from backend.config.settings import settings
from backend.Resume.schemas.candidate import CandidateProfile


class GroundingService:
    """
    Performs conservative source grounding against the original
    resume text.

    The principle is:

        Prefer an unresolved entity over a false positive.

    If deterministic matching cannot confidently establish that an
    extracted entity is present in the source document, the entity
    remains unresolved and can later be passed to the LLM verifier.
    """

    # TEXT NORMALIZATION
    
    @staticmethod
    def normalize_text(text: str) -> str:
        
        if not text:
            return ""

        text = text.lower().strip()

        # Normalize whitespace.
        text = re.sub(r"\s+", " ", text)

        # Normalize common Unicode punctuation.
        text = text.replace("–", "-")
        text = text.replace("—", "-")
        text = text.replace("’", "'")
        text = text.replace("“", '"')
        text = text.replace("”", '"')

        return text.strip()


    # SAFE TEXT VARIANTS
    
    @staticmethod
    def generate_safe_variants(value: str) -> List[str]:
        
        normalized = GroundingService.normalize_text(value)

        if not normalized:
            return []

        variants = {normalized}

        # "react.js" -> "react js"
        if "." in normalized:
            variants.add(
                normalized.replace(".", " ")
            )

        # "react js" -> "reactjs"
        if " " in normalized:
            variants.add(
                normalized.replace(" ", "")
            )

        if " " in normalized:
            variants.add(
                normalized.replace(" ", ".")
            )

        # "node-js" -> "node js"
        if "-" in normalized:
            variants.add(
                normalized.replace("-", " ")
            )

        # "node js" -> "node-js"
        if " " in normalized:
            variants.add(
                normalized.replace(" ", "-")
            )

        return list(variants)

    
    # ENTITY MATCHING
    
    @classmethod
    def find_entity_in_text(cls, entity: str, source_text: str) -> bool:
        if not entity or not source_text:
            return False

        normalized_source = cls.normalize_text(source_text)

        if not normalized_source:
            return False

        variants = cls.generate_safe_variants(entity)

        for variant in variants:

            # Do not treat a bare word as grounded when it is
            # immediately followed by a dot, e.g.:
            # Node -> Node.js
            if "." not in variant:
                dotted_prefix_pattern = rf"(?<!\w){re.escape(variant)}\."
                if re.search(dotted_prefix_pattern, normalized_source):
                    continue

            if cls.contains_as_phrase(
                phrase=variant,
                source_text=normalized_source,
            ):
                return True

        return False

    @staticmethod
    def contains_as_phrase(phrase: str,source_text: str) -> bool:
        
        if not phrase or not source_text:
            return False

        escaped_phrase = re.escape(phrase)

        pattern = rf"(?<!\w){escaped_phrase}(?!\w)"

        return (
            re.search(
                pattern,
                source_text,
            )
            is not None
        )

  
    # SKILL GROUNDING
   
    def ground_skills(self,skills: List[str],resume_text: str,) -> Tuple[List[str], List[str]]:
        
        grounded: List[str] = []
        unresolved: List[str] = []

        for skill in skills:

            if self.find_entity_in_text(
                entity=skill,
                source_text=resume_text,
            ):
                grounded.append(skill)
            else:
                unresolved.append(skill)

        return grounded, unresolved

   
    # PROJECT TITLE GROUNDING
   
    def ground_project_title(self,title: str,resume_text: str) -> bool:
        
        if not title or not resume_text:
            return False

        normalized_resume = self.normalize_text(resume_text)

        variants = self.generate_safe_variants(title)

        for variant in variants:

            if self.contains_as_phrase(
                phrase=variant,
                source_text=normalized_resume,
            ):
                return True

        return False

    
    # PROJECT TECHNOLOGY GROUNDING
   

    def ground_project_technologies(self,technologies: List[str],resume_text: str) -> Tuple[List[str], List[str]]:
        
        grounded: List[str] = []
        unresolved: List[str] = []

        for technology in technologies:

            if self.find_entity_in_text(
                entity=technology,
                source_text=resume_text,
            ):
                grounded.append(technology)
            else:
                unresolved.append(technology)

        return grounded, unresolved

    
    # FULL PROFILE GROUNDING
 

    def ground(self,candidate: CandidateProfile,resume_text: str) -> Dict:
        
        result = {
            "skills": {
                "grounded": [],
                "unresolved": [],
            },
            "projects": [],
        }

        # Skills
      
        grounded_skills, unresolved_skills = (
            self.ground_skills(
                skills=candidate.skills,
                resume_text=resume_text,
            )
        )

        result["skills"]["grounded"] = (
            grounded_skills
        )

        result["skills"]["unresolved"] = (
            unresolved_skills
        )

       
        # Projects
       
        for project in candidate.projects:

            grounded_technologies, unresolved_technologies = (
                self.ground_project_technologies(
                    technologies=project.technologies,
                    resume_text=resume_text,
                )
            )

            project_result = {
                "title": project.title,

                "title_grounded": (
                    self.ground_project_title(
                        title=project.title,
                        resume_text=resume_text,
                    )
                ),

                "technologies": {
                    "grounded": (
                        grounded_technologies
                    ),
                    "unresolved": (
                        unresolved_technologies
                    ),
                },
            }

            result["projects"].append(
                project_result
            )

        return result

    
    # LLM VERIFIER
   

    def verify_unresolved_entities(self,entities: List[str],resume_text: str,) -> List[Dict]:
        """
        Use an LLM to verify entities that could not be grounded
        deterministically.

        IMPORTANT:

        The LLM is acting as a VERIFIER, not an extractor.

        It must use only the supplied resume text.

        Returns:

            [
                {
                    "entity": "PostgreSQL",
                    "status": "SUPPORTED",
                    "reason": "The resume mentions Postgres."
                },
                {
                    "entity": "MongoDB",
                    "status": "UNSUPPORTED",
                    "reason": "MongoDB is not supported by the resume."
                }
            ]
        """

        # No entities need verification.
        if not entities:
            return []

        # No resume available means we cannot verify anything.
        if not resume_text:
            return [
                {
                    "entity": entity,
                    "status": "UNCERTAIN",
                    "reason": (
                        "Resume text was unavailable."
                    ),
                }
                for entity in entities
            ]

        # Remove duplicates while preserving order.
        unique_entities = list(
            dict.fromkeys(entities)
        )

        entities_json = json.dumps(
            unique_entities,
            ensure_ascii=False,
        )

        # Verifier System Prompt
       
        system_prompt = """
You are a source-grounding verifier for a resume
intelligence system.

Your ONLY job is to verify whether the extracted entities
are supported by the ORIGINAL resume.

You are NOT an extractor.

For every entity, return exactly one status:

SUPPORTED
    The resume explicitly supports the entity.

UNSUPPORTED
    The resume does not support the entity.

UNCERTAIN
    The resume contains related or ambiguous information,
    but there is not enough evidence to confidently establish
    that the extracted entity is supported.

IMPORTANT RULES:

1. Use ONLY the supplied resume.

2. Do NOT use outside knowledge.

3. Do NOT invent information.

4. Do NOT assume that two technologies are equivalent unless
   the resume itself provides enough evidence.

5. A related technology does not automatically prove that the
   candidate knows the extracted technology.

6. "Java" must NOT be considered supported merely because
   "JavaScript" appears.

7. "Machine Learning" must NOT automatically be considered
   supported merely because "AI" appears.

8. If the evidence is insufficient, use UNCERTAIN.

9. Be conservative.

10. Return exactly one result for every supplied entity.

11. Return ONLY valid JSON.

Required format:

{
    "results": [
        {
            "entity": "string",
            "status": "SUPPORTED",
            "reason": "short explanation"
        }
    ]
}

The status MUST be exactly one of:

SUPPORTED
UNSUPPORTED
UNCERTAIN
"""

        # Verifier Human Prompt
        

        human_prompt = f"""
ORIGINAL RESUME:

{resume_text}


EXTRACTED ENTITIES TO VERIFY:

{entities_json}


TASK:

Verify every extracted entity against the original resume.

Determine whether each entity is:

SUPPORTED,
UNSUPPORTED,
or UNCERTAIN.

Do not extract additional skills.
Do not add entities that are not in the supplied list.
"""

        messages = [
            SystemMessage(
                content=system_prompt
            ),
            HumanMessage(
                content=human_prompt
            ),
        ]

        
        # LLM Invocation
        
        try:

            response = settings.llm.invoke(
                messages
            )

            content = response.content

            if not isinstance(content, str):
                raise ValueError(
                    "LLM verifier returned "
                    "non-string content."
                )

            content = content.strip()

           
            # Remove accidental markdown code fences
           

            if content.startswith("```"):

                content = re.sub(
                    r"^```(?:json)?\s*",
                    "",
                    content,
                    flags=re.IGNORECASE,
                )

                content = re.sub(
                    r"\s*```$",
                    "",
                    content,
                )

                content = content.strip()

 
            # Parse JSON
           

            data = json.loads(content)

            if not isinstance(data, dict):
                raise ValueError(
                    "LLM verifier returned a "
                    "non-object JSON response."
                )

            results = data.get(
                "results",
                [],
            )

            if not isinstance(
                results,
                list,
            ):
                raise ValueError(
                    "LLM verifier returned an "
                    "invalid results format."
                )

            
            # Validate verifier results
        

            allowed_statuses = {
                "SUPPORTED",
                "UNSUPPORTED",
                "UNCERTAIN",
            }

            validated_results: List[Dict] = []

            for result in results:

                if not isinstance(
                    result,
                    dict,
                ):
                    continue

                entity = result.get(
                    "entity"
                )

                status = result.get(
                    "status"
                )

                reason = result.get(
                    "reason"
                )

                if not isinstance(
                    entity,
                    str,
                ):
                    continue

                entity = entity.strip()

                if not entity:
                    continue

                # Invalid status becomes UNCERTAIN.
                if status not in allowed_statuses:
                    status = "UNCERTAIN"

                if not isinstance(
                    reason,
                    str,
                ):
                    reason = ""

                validated_results.append(
                    {
                        "entity": entity,
                        "status": status,
                        "reason": reason.strip(),
                    }
                )

            # Ensure every requested entity has a result
           

            returned_entities = {
                result["entity"].strip().lower()
                for result in validated_results
            }

            for entity in unique_entities:

                if (
                    entity.strip().lower()
                    not in returned_entities
                ):
                    validated_results.append(
                        {
                            "entity": entity,
                            "status": "UNCERTAIN",
                            "reason": (
                                "Verifier did not "
                                "return a result "
                                "for this entity."
                            ),
                        }
                    )

            return validated_results

        except Exception as error:

            # IMPORTANT:
            #
            # If the verifier itself fails, we must NOT mark
            # the entities as UNSUPPORTED.
            #
            # Otherwise a temporary LLM/API/JSON failure could
            # incorrectly remove valid resume information.

            return [
                {
                    "entity": entity,
                    "status": "UNCERTAIN",
                    "reason": (
                        "LLM verification failed: "
                        f"{str(error)}"
                    ),
                }
                for entity in unique_entities
            ]

    
    # COMPLETE GROUNDING + LLM VERIFICATION
    

    def ground_with_verifier(self,candidate: CandidateProfile,resume_text: str,) -> Dict:
        """
        Perform deterministic grounding first.

        Only unresolved entities are sent to the LLM verifier.

        The CandidateProfile is NOT modified.
        """

       
        # Step 1: Deterministic grounding

        result = self.ground(
            candidate=candidate,
            resume_text=resume_text,
        )

        # Step 2: Collect unresolved skills
       

        unresolved_entities: List[str] = []

        unresolved_entities.extend(
            result["skills"]["unresolved"]
        )

      
        # Step 3: Collect unresolved project technologies
       

        for project in result["projects"]:

            unresolved_entities.extend(
                project["technologies"]["unresolved"]
            )

        
        # Step 4: Remove duplicates
       

        unresolved_entities = list(
            dict.fromkeys(
                unresolved_entities
            )
        )

     
        # Step 5: LLM verification
    
        verification_results = (
            self.verify_unresolved_entities(
                entities=unresolved_entities,
                resume_text=resume_text,
            )
        )

        # Step 6: Store verifier results
       
        result["llm_verification"] = (
            verification_results
        )

        return result