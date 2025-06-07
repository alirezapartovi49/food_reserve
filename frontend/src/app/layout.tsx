import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { getMe, getUserFoods } from "@/utils/utils";
import { cookies } from "next/headers";
import { userType } from "@/types/user.type";

export const metadata: Metadata = {
  title: "سماد | سامانه مدیریت امور دانشجویی",
  description: "سماد | سامانه مدیریت امور دانشجویی",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const user = await getMe();
  const userFoods = await getUserFoods();

  const cookiesHeader = await cookies();
  const token = cookiesHeader.get("token")?.value;

  return (
    <html lang="fa" dir="rtl">
      <body className={`antialiased`}>
        <Providers user={user ? ({ ...user, token, reserved_foods: userFoods } as userType) : null}>{children}</Providers>
      </body>
    </html>
  );
}
