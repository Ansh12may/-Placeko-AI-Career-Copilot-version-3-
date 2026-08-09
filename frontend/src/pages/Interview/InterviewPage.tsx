import {
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { useNavigate, useParams } from "react-router-dom";

import {
  CheckCircle2,
  Clock3,
  MessageSquare,
  Mic,
  RotateCcw,
  Send,
  Sparkles,
  Square,
  Volume2,
} from "lucide-react";

import {
  getInterviewSession,
  submitInterviewAnswer,
  submitVoiceAnswer,
  finishInterview,
} from "../../api/interview";

import type {
  InterviewSession,
} from "../../types/interview";


const InterviewPage = () => {
  const navigate = useNavigate();

  const { sessionId } = useParams<{
    sessionId: string;
  }>();

  // =========================================================
  // Interview State
  // =========================================================

  const [session, setSession] =
    useState<InterviewSession | null>(null);

  const [answer, setAnswer] =
    useState("");

  const [answerMode, setAnswerMode] =
    useState<"text" | "voice">("text");

  // =========================================================
  // Voice Recording State
  // =========================================================

  const [isRecording, setIsRecording] =
    useState(false);

  const [audioBlob, setAudioBlob] =
    useState<Blob | null>(null);

  const [audioUrl, setAudioUrl] =
    useState<string | null>(null);

  const [recordingSeconds, setRecordingSeconds] =
    useState(0);

  const mediaRecorderRef =
    useRef<MediaRecorder | null>(null);

  const mediaStreamRef =
    useRef<MediaStream | null>(null);

  const audioChunksRef =
    useRef<Blob[]>([]);

  const recordingTimerRef =
    useRef<ReturnType<typeof setInterval> | null>(
      null
    );

  // =========================================================
  // Loading / Submission State
  // =========================================================

  const [isLoading, setIsLoading] =
    useState(true);

  const [isSubmitting, setIsSubmitting] =
    useState(false);

  const [isFinishing, setIsFinishing] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  // =========================================================
  // Load Interview Session
  // =========================================================

  useEffect(() => {
    if (!sessionId) {
      setError(
        "Interview session not found."
      );

      setIsLoading(false);

      return;
    }

    const loadSession = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data =
          await getInterviewSession(
            sessionId
          );

        setSession(data);

      } catch (err) {
        console.error(
          "Failed to load interview session:",
          err
        );

        setError(
          "Unable to load the interview."
        );

      } finally {
        setIsLoading(false);
      }
    };

    loadSession();
  }, [sessionId]);

  // =========================================================
  // Cleanup Voice Resources
  // =========================================================

  useEffect(() => {
    return () => {
      // Stop timer
      if (recordingTimerRef.current) {
        clearInterval(
          recordingTimerRef.current
        );

        recordingTimerRef.current = null;
      }

      // Stop recorder
      const recorder =
        mediaRecorderRef.current;

      if (
        recorder &&
        recorder.state === "recording"
      ) {
        recorder.stop();
      }

      // Stop microphone stream
      if (mediaStreamRef.current) {
        mediaStreamRef.current
          .getTracks()
          .forEach((track) => {
            track.stop();
          });

        mediaStreamRef.current = null;
      }

      // Revoke audio URL
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  // =========================================================
  // Current Question
  // =========================================================

  const currentPair = useMemo(() => {
    if (!session) {
      return null;
    }

    return (
      session.history[
        session.current_question_index
      ] ?? null
    );
  }, [session]);

  const currentQuestion =
    currentPair?.question ?? null;

  // =========================================================
  // Progress
  // =========================================================

  const questionNumber =
    session
      ? session.current_question_index + 1
      : 0;

  const totalQuestions =
    session
      ? session.interview_plan
          .technical_questions +
        session.interview_plan
          .behavioral_questions +
        session.interview_plan
          .project_questions
      : 0;

  const progress =
    totalQuestions > 0
      ? Math.min(
          (questionNumber /
            totalQuestions) *
            100,
          100
        )
      : 0;

  // =========================================================
  // Recording Time Formatter
  // =========================================================

  const formatRecordingTime = (
    seconds: number
  ): string => {
    const minutes =
      Math.floor(seconds / 60);

    const remainingSeconds =
      seconds % 60;

    return `${String(minutes).padStart(
      2,
      "0"
    )}:${String(
      remainingSeconds
    ).padStart(2, "0")}`;
  };

  // =========================================================
  // Select Supported Recording Format
  // =========================================================

  const getSupportedMimeType = (): string => {
    const mimeTypes = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg;codecs=opus",
    ];

    for (const mimeType of mimeTypes) {
      if (
        MediaRecorder.isTypeSupported(
          mimeType
        )
      ) {
        return mimeType;
      }
    }

    return "";
  };

  // =========================================================
  // Start Voice Recording
  // =========================================================

  const startRecording = async () => {
    try {
      setError(null);

      // -----------------------------------------------------
      // Browser support
      // -----------------------------------------------------

      if (
        !navigator.mediaDevices ||
        !navigator.mediaDevices.getUserMedia
      ) {
        setError(
          "Your browser does not support microphone recording."
        );

        return;
      }

      if (
        typeof MediaRecorder ===
        "undefined"
      ) {
        setError(
          "Your browser does not support audio recording."
        );

        return;
      }

      // -----------------------------------------------------
      // Request microphone access
      // -----------------------------------------------------

      const stream =
        await navigator.mediaDevices.getUserMedia(
          {
            audio: true,
          }
        );

      mediaStreamRef.current =
        stream;

      // -----------------------------------------------------
      // Determine supported MIME type
      // -----------------------------------------------------

      const mimeType =
        getSupportedMimeType();

      const recorder =
        mimeType
          ? new MediaRecorder(
              stream,
              {
                mimeType,
              }
            )
          : new MediaRecorder(
              stream
            );

      audioChunksRef.current = [];

      // -----------------------------------------------------
      // Clear previous recording
      // -----------------------------------------------------

      if (audioUrl) {
        URL.revokeObjectURL(
          audioUrl
        );
      }

      setAudioUrl(null);
      setAudioBlob(null);
      setRecordingSeconds(0);

      // -----------------------------------------------------
      // Collect audio chunks
      // -----------------------------------------------------

      recorder.ondataavailable = (
        event
      ) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(
            event.data
          );
        }
      };

      // -----------------------------------------------------
      // Handle recording stop
      // -----------------------------------------------------

      recorder.onstop = () => {
        const finalMimeType =
          recorder.mimeType ||
          mimeType ||
          "audio/webm";

        const blob = new Blob(
          audioChunksRef.current,
          {
            type: finalMimeType,
          }
        );

        setAudioBlob(blob);

        const url =
          URL.createObjectURL(
            blob
          );

        setAudioUrl(url);

        // Stop microphone
        if (
          mediaStreamRef.current
        ) {
          mediaStreamRef.current
            .getTracks()
            .forEach((track) => {
              track.stop();
            });

          mediaStreamRef.current =
            null;
        }
      };

      // -----------------------------------------------------
      // Handle recorder error
      // -----------------------------------------------------

      recorder.onerror = (
        event
      ) => {
        console.error(
          "MediaRecorder error:",
          event
        );

        setError(
          "An error occurred while recording your answer."
        );

        setIsRecording(false);
      };

      mediaRecorderRef.current =
        recorder;

      // -----------------------------------------------------
      // Start recording
      // -----------------------------------------------------

      recorder.start();

      setIsRecording(true);

      // -----------------------------------------------------
      // Start timer
      // -----------------------------------------------------

      if (
        recordingTimerRef.current
      ) {
        clearInterval(
          recordingTimerRef.current
        );
      }

      recordingTimerRef.current =
        setInterval(() => {
          setRecordingSeconds(
            (seconds) =>
              seconds + 1
          );
        }, 1000);

    } catch (err) {
      console.error(
        "Failed to start recording:",
        err
      );

      // Clean up stream if microphone
      // permission fails or recorder creation fails.

      if (
        mediaStreamRef.current
      ) {
        mediaStreamRef.current
          .getTracks()
          .forEach((track) => {
            track.stop();
          });

        mediaStreamRef.current =
          null;
      }

      setIsRecording(false);

      setError(
        "Microphone access was denied or is unavailable."
      );
    }
  };

  // =========================================================
  // Stop Voice Recording
  // =========================================================

  const stopRecording = () => {
    const recorder =
      mediaRecorderRef.current;

    if (!recorder) {
      return;
    }

    if (
      recorder.state ===
      "recording"
    ) {
      recorder.stop();
    }

    setIsRecording(false);

    if (
      recordingTimerRef.current
    ) {
      clearInterval(
        recordingTimerRef.current
      );

      recordingTimerRef.current =
        null;
    }
  };

  // =========================================================
  // Reset Voice Recording
  // =========================================================

  const resetRecording = () => {
    if (isRecording) {
      return;
    }

    setAudioBlob(null);

    setRecordingSeconds(0);

    audioChunksRef.current = [];

    if (audioUrl) {
      URL.revokeObjectURL(
        audioUrl
      );

      setAudioUrl(null);
    }
  };

  // =========================================================
  // Switch Answer Mode
  // =========================================================

  const handleAnswerModeChange = (
    mode: "text" | "voice"
  ) => {
    if (
      isSubmitting ||
      isFinishing ||
      isRecording
    ) {
      return;
    }

    setAnswerMode(mode);

    setError(null);
  };

  // =========================================================
  // Submit Text Answer
  // =========================================================

  const handleSubmitAnswer =
    async () => {
      if (
        !session ||
        !currentQuestion
      ) {
        return;
      }

      if (!answer.trim()) {
        setError(
          "Please enter an answer before submitting."
        );

        return;
      }

      try {
        setIsSubmitting(true);
        setError(null);

        const updatedSession =
          await submitInterviewAnswer(
            session.session_id,
            {
              question_id:
                currentQuestion.question_id,

              transcript:
                answer.trim(),

              source: "Text",

              duration_seconds: 0,

              metadata: null,
            }
          );

        setAnswer("");

        setSession(
          updatedSession
        );

        // ---------------------------------------------------
        // Interview completed
        // ---------------------------------------------------

        if (
          updatedSession.status ===
          "Completed"
        ) {
          await handleFinishInterview(
            updatedSession.session_id
          );
        }

      } catch (err) {
        console.error(
          "Failed to submit answer:",
          err
        );

        setError(
          "Unable to submit your answer. Please try again."
        );

      } finally {
        setIsSubmitting(false);
      }
    };

  // =========================================================
  // Submit Voice Answer
  // =========================================================

  const handleSubmitVoiceAnswer =
    async () => {
      if (
        !session ||
        !currentQuestion
      ) {
        return;
      }

      if (!audioBlob) {
        setError(
          "Please record your answer before submitting."
        );

        return;
      }

      try {
        setIsSubmitting(true);
        setError(null);

        // ---------------------------------------------------
        // Build multipart form data
        // ---------------------------------------------------

        const formData =
          new FormData();

        formData.append(
          "audio",
          audioBlob,
          "interview-answer.webm"
        );

        formData.append(
          "question_id",
          String(
            currentQuestion.question_id
          )
        );

        // ---------------------------------------------------
        // Send voice answer
        // ---------------------------------------------------

        const updatedSession =
          await submitVoiceAnswer(
            session.session_id,
            formData
          );

        // ---------------------------------------------------
        // Clear old recording
        // ---------------------------------------------------

        resetRecording();

        setSession(
          updatedSession
        );

        // ---------------------------------------------------
        // Interview completed
        // ---------------------------------------------------

        if (
          updatedSession.status ===
          "Completed"
        ) {
          await handleFinishInterview(
            updatedSession.session_id
          );
        }

      } catch (err) {
        console.error(
          "Failed to submit voice answer:",
          err
        );

        setError(
          "Unable to submit your voice answer. Please try again."
        );

      } finally {
        setIsSubmitting(false);
      }
    };

  // =========================================================
  // Finish Interview
  // =========================================================

  const handleFinishInterview =
    async (
      currentSessionId?: string
    ) => {
      const id =
        currentSessionId ??
        session?.session_id;

      if (!id) {
        return;
      }

      try {
        setIsFinishing(true);
        setError(null);

        await finishInterview(id);

        navigate(
          `/interview/${id}/report`
        );

      } catch (err) {
        console.error(
          "Failed to finish interview:",
          err
        );

        setError(
          "Interview completed, but the report could not be generated."
        );

      } finally {
        setIsFinishing(false);
      }
    };

  // =========================================================
  // Loading
  // =========================================================

  if (isLoading) {
    return (
      <div className="flex min-h-[600px] items-center justify-center">
        <div className="text-sm font-medium text-slate-500">
          Preparing your interview...
        </div>
      </div>
    );
  }

  // =========================================================
  // Error Without Session
  // =========================================================

  if (error && !session) {
    return (
      <div className="flex min-h-[600px] items-center justify-center">
        <div className="max-w-md rounded-2xl border border-red-200 bg-red-50 p-6 text-center">

          <p className="text-sm font-semibold text-red-600">
            {error}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate("/interview")
            }
            className="mt-5 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white"
          >
            Back to Interview Setup
          </button>

        </div>
      </div>
    );
  }

  // =========================================================
  // Invalid Session
  // =========================================================

  if (
    !session ||
    !currentQuestion
  ) {
    return (
      <div className="flex min-h-[600px] items-center justify-center">
        <p className="text-sm text-slate-500">
          No active interview question found.
        </p>
      </div>
    );
  }

  // =========================================================
  // Main UI
  // =========================================================

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">

      {/* =====================================================
          Header
          ===================================================== */}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>

          <div className="flex items-center gap-2">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
              <Sparkles size={18} />
            </div>

            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
              AI Interview
            </span>

          </div>

          <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-950 dark:text-white">
            Mock Interview
          </h1>

        </div>

        <div className="flex items-center gap-3">

          <div className="flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-xs font-semibold text-slate-600">
            <Clock3 size={14} />

            {session.interview_plan.duration_minutes}{" "}
            min
          </div>

          <div className="rounded-full bg-indigo-50 px-4 py-2 text-xs font-bold text-indigo-600">
            {questionNumber} / {totalQuestions}
          </div>

        </div>

      </div>

      {/* =====================================================
          Progress
          ===================================================== */}

      <div>

        <div className="mb-2 flex items-center justify-between text-xs">

          <span className="font-medium text-slate-500">
            Interview Progress
          </span>

          <span className="font-bold text-slate-700">
            {Math.round(progress)}%
          </span>

        </div>

        <div className="h-2 overflow-hidden rounded-full bg-slate-100">

          <div
            className="h-full rounded-full bg-indigo-600 transition-all duration-500"
            style={{
              width: `${progress}%`,
            }}
          />

        </div>

      </div>

      {/* =====================================================
          Error
          ===================================================== */}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {/* =====================================================
          Question
          ===================================================== */}

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900 sm:p-8">

        <div className="flex items-start justify-between gap-4">

          <div className="flex items-center gap-2">

            <span className="rounded-full bg-indigo-50 px-3 py-1 text-[11px] font-bold uppercase tracking-wide text-indigo-600">
              {currentQuestion.category}
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-semibold text-slate-500">
              {currentQuestion.difficulty}
            </span>

          </div>

          <span className="text-xs font-medium text-slate-400">
            Question{" "}
            {currentQuestion.question_id}
          </span>

        </div>

        <div className="mt-8 flex gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white">
            <MessageSquare size={20} />
          </div>

          <div>

            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
              AI Interviewer
            </p>

            <h2 className="mt-2 text-xl font-bold leading-8 text-slate-950 dark:text-white sm:text-2xl">
              {currentQuestion.question}
            </h2>

          </div>

        </div>

        {/* Focus */}

        <div className="mt-6 rounded-xl bg-slate-50 p-4">

          <p className="text-[11px] font-bold uppercase tracking-wide text-slate-400">
            Focus Topic
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {currentQuestion.focus_topic}
          </p>

        </div>

      </div>

      {/* =====================================================
          Answer
          ===================================================== */}

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">

        {/* ===================================================
            Answer Header
            =================================================== */}

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

          <div>

            <h2 className="text-base font-bold text-slate-900 dark:text-white">
              Your Answer
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Choose how you want to answer this question.
            </p>

          </div>

          {/* Answer Mode */}

          <div className="flex rounded-xl bg-slate-100 p-1">

            <button
              type="button"
              onClick={() =>
                handleAnswerModeChange(
                  "text"
                )
              }
              disabled={
                isSubmitting ||
                isFinishing ||
                isRecording
              }
              className={`flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-semibold transition ${
                answerMode === "text"
                  ? "bg-white text-indigo-600 shadow-sm"
                  : "text-slate-500 hover:text-slate-700"
              }`}
            >
              <MessageSquare
                size={14}
              />

              Text
            </button>

            <button
              type="button"
              onClick={() =>
                handleAnswerModeChange(
                  "voice"
                )
              }
              disabled={
                isSubmitting ||
                isFinishing ||
                isRecording
              }
              className={`flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-semibold transition ${
                answerMode === "voice"
                  ? "bg-white text-indigo-600 shadow-sm"
                  : "text-slate-500 hover:text-slate-700"
              }`}
            >
              <Mic size={14} />

              Voice
            </button>

          </div>

        </div>

        {/* ===================================================
            TEXT MODE
            =================================================== */}

        {answerMode === "text" && (
          <>
            <div className="mt-5 flex justify-end">

              <span className="text-xs text-slate-400">
                {answer.trim().length}{" "}
                characters
              </span>

            </div>

            <textarea
              value={answer}
              onChange={(event) =>
                setAnswer(
                  event.target.value
                )
              }
              placeholder="Type your answer here..."
              rows={9}
              disabled={
                isSubmitting ||
                isFinishing
              }
              className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-7 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:cursor-not-allowed disabled:opacity-60"
            />

            <div className="mt-5 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-between">

              <button
                type="button"
                onClick={() =>
                  navigate("/interview")
                }
                disabled={
                  isSubmitting ||
                  isFinishing
                }
                className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:border-slate-300 hover:text-slate-900 disabled:opacity-50"
              >
                Exit Interview
              </button>

              <button
                type="button"
                onClick={
                  handleSubmitAnswer
                }
                disabled={
                  isSubmitting ||
                  isFinishing ||
                  !answer.trim()
                }
                className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
              >

                <Send size={16} />

                {isSubmitting
                  ? "Evaluating..."
                  : "Submit Answer"}

              </button>

            </div>
          </>
        )}

        {/* ===================================================
            VOICE MODE
            =================================================== */}

        {answerMode === "voice" && (
          <div className="mt-5">

            {/* Recording Area */}

            <div className="rounded-2xl border border-indigo-100 bg-indigo-50/50 p-8">

              <div className="flex flex-col items-center text-center">

                {/* Microphone */}

                <div
                  className={`flex h-20 w-20 items-center justify-center rounded-full transition ${
                    isRecording
                      ? "bg-red-100 text-red-600"
                      : audioBlob
                        ? "bg-emerald-100 text-emerald-600"
                        : "bg-indigo-100 text-indigo-600"
                  }`}
                >
                  <Mic size={32} />
                </div>

                {/* Status */}

                <h3 className="mt-5 text-base font-bold text-slate-900">

                  {isRecording
                    ? "Recording your answer..."
                    : audioBlob
                      ? "Answer recorded"
                      : "Ready to record"}

                </h3>

                <p className="mt-2 max-w-md text-xs leading-6 text-slate-500">

                  {isRecording
                    ? "Speak clearly and explain your reasoning. Stop recording when you are finished."
                    : audioBlob
                      ? "Listen to your recording or record it again before submitting."
                      : "Answer naturally as if you were in a real interview."}

                </p>

                {/* Timer */}

                <div
                  className={`mt-5 flex items-center gap-2 rounded-full px-4 py-2 text-sm font-bold ${
                    isRecording
                      ? "bg-red-100 text-red-600"
                      : "bg-white text-slate-600"
                  }`}
                >

                  <Clock3 size={15} />

                  {formatRecordingTime(
                    recordingSeconds
                  )}

                </div>

                {/* Recording Controls */}

                <div className="mt-6 flex flex-wrap items-center justify-center gap-3">

                  {/* Start */}

                  {!isRecording &&
                    !audioBlob && (
                      <button
                        type="button"
                        onClick={
                          startRecording
                        }
                        disabled={
                          isSubmitting ||
                          isFinishing
                        }
                        className="flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                      >

                        <Mic size={17} />

                        Start Recording

                      </button>
                    )}

                  {/* Stop */}

                  {isRecording && (
                    <button
                      type="button"
                      onClick={
                        stopRecording
                      }
                      disabled={
                        isSubmitting ||
                        isFinishing
                      }
                      className="flex items-center gap-2 rounded-xl bg-red-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >

                      <Square
                        size={15}
                        fill="currentColor"
                      />

                      Stop Recording

                    </button>
                  )}

                  {/* Recorded */}

                  {!isRecording &&
                    audioBlob && (
                      <>
                        <button
                          type="button"
                          onClick={
                            resetRecording
                          }
                          disabled={
                            isSubmitting ||
                            isFinishing
                          }
                          className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-600 transition hover:border-indigo-300 hover:text-indigo-600 disabled:opacity-50"
                        >

                          <RotateCcw
                            size={15}
                          />

                          Re-record

                        </button>

                        <button
                          type="button"
                          onClick={
                            handleSubmitVoiceAnswer
                          }
                          disabled={
                            isSubmitting ||
                            isFinishing
                          }
                          className="flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                        >

                          <Send
                            size={16}
                          />

                          {isSubmitting
                            ? "Evaluating..."
                            : "Submit Voice Answer"}

                        </button>
                      </>
                    )}

                </div>

              </div>

            </div>

            {/* Audio Preview */}

            {audioBlob &&
              audioUrl && (
                <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4">

                  <div className="flex items-center gap-3">

                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-indigo-600">

                      <Volume2
                        size={17}
                      />

                    </div>

                    <div className="min-w-0 flex-1">

                      <p className="text-xs font-bold text-slate-700">
                        Recorded Answer
                      </p>

                      <p className="mt-0.5 text-[11px] text-slate-400">
                        {formatRecordingTime(
                          recordingSeconds
                        )}
                      </p>

                    </div>

                  </div>

                  <audio
                    controls
                    src={audioUrl}
                    className="mt-3 w-full"
                  />

                </div>
              )}

            {/* Exit */}

            <div className="mt-5 flex justify-start">

              <button
                type="button"
                onClick={() =>
                  navigate("/interview")
                }
                disabled={
                  isSubmitting ||
                  isFinishing ||
                  isRecording
                }
                className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:border-slate-300 hover:text-slate-900 disabled:opacity-50"
              >
                Exit Interview
              </button>

            </div>

          </div>
        )}

      </div>

      {/* =====================================================
          Interview Tips
          ===================================================== */}

      <div className="rounded-2xl border border-indigo-100 bg-indigo-50/60 p-5">

        <div className="flex gap-3">

          <CheckCircle2
            size={18}
            className="mt-0.5 shrink-0 text-indigo-600"
          />

          <div>

            <p className="text-sm font-bold text-slate-800">
              Interview tip
            </p>

            <p className="mt-1 text-xs leading-6 text-slate-600">
              Structure your answer clearly.
              Explain what you did, why you
              did it, and the result. Use
              specific examples from your
              projects whenever possible.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
};

export default InterviewPage;