"use server";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const login = async (prevState: any, formData: FormData) => {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PATH}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: formData.get("email"),
        password: formData.get("password"),
      }),
    });

    if (res.status === 401) {
      return {
        error: "user not found",
        status: 401,
        success: false,
      };
    } else if (res.status === 200) {
      const data = await res.json();

      const cookiesHeader = await cookies();
      cookiesHeader.set("token", data.token, { httpOnly: true, maxAge: 5 * 24 * 60 * 60 });

      return {
        error: undefined,
        status: 200,
        success: true,
        data,
      };
    }
  } catch (err) {
    return {
      error: "Internal Server Error",
      status: 500,
      success: false,
    };
  }
};

export const logout = async () => {
  const cookiesHeader = await cookies();

  cookiesHeader.delete("token");

  redirect("/login");
};
