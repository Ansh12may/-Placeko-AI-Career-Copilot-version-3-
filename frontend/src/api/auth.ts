import api from "./axios.ts";

export interface LoginResponse {
  success: boolean;
  message: string;
  data: {
    user_id: string;
    access_token: string;
    refresh_token: string;
  };

}


export interface RegisterResponse {
  success: boolean;
  message: string;
  data: {
    user_id: string;
    access_token: string;
    refresh_token: string;
  };

}

export interface User {
  id: string;
  full_name: string;
  email: string;
  avatar: string | null;
  provider: string;
  email_verified: boolean;
}

interface CurrentUserResponse {
  success: boolean;
  data: User;
}



export const login = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>(
    "/api/auth/login",
    {
      email,
      password,
    }

  );
  return response.data;

};


export const register = async (
  fullName: string,
  email: string,
  password: string
): Promise<RegisterResponse> => {
  const response = await api.post<RegisterResponse>(
    "/api/auth/register",
    {
      full_name: fullName,
      email,
      password,

    }
  );
  return response.data;

};



export const getCurrentUser = async (): Promise<User> => {
  const token = localStorage.getItem("access_token");
  const response = await api.get<CurrentUserResponse>(
    "/api/auth/me",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data.data;
};



export const logout = async (): Promise<void> => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return;
  }
  await api.post(
    "/api/auth/logout",
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};


