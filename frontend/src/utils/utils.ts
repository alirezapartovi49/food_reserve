import { userType } from "@/types/user.type";
import { cookies } from "next/headers";

export const getMe = async (): Promise<userType | null> => {
  const cookiesHeader = await cookies();
  const token = cookiesHeader.get("token")?.value;

  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PATH}/accounts/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!res.ok) {
      return null;
    }

    const data = await res.json();

    return data;
  } catch (err) {
    return null;
  }
};

export const getUserFoods = async () => {
  const cookiesHeader = await cookies();
  const token = cookiesHeader.get("token")?.value;

  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PATH}/reserve/reserve`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!res.ok) {
      return null;
    }

    const data = await res.json();

    return data;
  } catch (err) {
    return null;
  }
};
