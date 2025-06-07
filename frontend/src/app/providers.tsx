"use client";
import { HeroUIProvider } from "@heroui/react";
import { Toaster } from "react-hot-toast";
import { UserContext } from "@/contexts/auth";
import { userType } from "@/types/user.type";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

export function Providers({ children, user }: { children: React.ReactNode; user: userType | null }) {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <HeroUIProvider>
        <UserContext value={user}>
          <Toaster
            toastOptions={{
              className: "font-DanaMedium",
            }}
          />
          {children}
        </UserContext>
      </HeroUIProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
