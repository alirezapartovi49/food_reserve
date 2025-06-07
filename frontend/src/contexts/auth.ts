"use client";
import { createContext, use } from "react";
import { userType } from "@/types/user.type";

export const UserContext = createContext<userType | null>(null);

export const useUser = () => {
  const user = use(UserContext);

  return user;
};
