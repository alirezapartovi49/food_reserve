"use client";
import { useUser } from "@/contexts/auth";
import { userType } from "@/types/user.type";
import dynamic from "next/dynamic";
import Link from "next/link";
const DropDown = dynamic(() => import("./DropDown"));

function Header() {
  const user: userType | null = useUser();
  
  return (
    <header className="bg-primary border-b border-b-[#f8f8f8]">
      <div className="container flex items-center justify-between h-[70px] xl:h-[50px]">
        <Link href="/" className="flex gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="#404040" viewBox="0 0 47 31" style={{ fill: "rgb(255, 255, 255)" }} className="w-10">
            <path fill="inherit" d="m12.32 30.531 1.309-.272 1.254-.326 1.199-.381 1.09-.382 1.09-.491.982-.546.926-.546.873-.6.818-.655.764-.654.709-.71.709-.709.655-.763.763-.927.764-.927 1.308-1.908.054-.055.381-.546.055-.109.38-.546v-.054l1.42-2.072.708-.981.764-.981.764-.873.818-.872.872-.818.981-.764 1.036-.655 1.09-.654 1.254-.492 1.364-.43 1.473-.326 1.636-.273 1.8-.108 1.962-.055V0l-1.854.054-1.745.11-1.636.163-1.576.217-1.418.327-1.418.381-1.308.43-1.2.43-1.146.546-1.09.6-1.036.6-.981.655-.873.71-.872.708-.818.764-.764.763v.01l.055.055-.764.764-.655.818-1.253 1.636-1.2 1.636-1.09 1.576-.709 1.09-.654.981-.055.055-.655.872v.055l-.654.872h-.055l-.927 1.09-.491.492-.546.491-.546.43-.546.381-.6.381-.655.327-.654.327-.71.272-.763.218-.818.163-.873.163-.927.109-.981.054-1.036.055V7.96l1.036.054 1.036.11 1.036.271.98.327.928.491.927.492.872.655.764.709 2.4 2.4.98-1.419 1.746-2.563.927-1.308 1.036-1.308-1.8-1.745-.6-.6-.655-.546-.709-.546-.655-.491-.709-.43-.763-.43-.764-.381-.764-.327-.756-.34-.818-.271-.818-.218-.818-.163-.818-.164-.873-.109-.818-.054H0v30.802h7.852l1.576-.054 1.473-.11z" />
            <path fill="inherit" stroke="inherit" d="m33.229 18.493 11.919 11.87h-9.816L29.24 24.27l.508-.69.003-.003.71-.982.006-.009.006-.01 1.251-1.904.922-1.357z" />
          </svg>

          <span className="flex flex-col">
            <span className="font-DanaDemiBold text-white text-sm">سمــاد</span>
            <span className="font-DanaMedium text-white text-xs">سامانه مدیریت امور دانشجویی</span>
          </span>
        </Link>
        {user ? <DropDown username={user?.fullname as string} userid={user?.id as string | number} /> : ""}
      </div>
    </header>
  );
}

export default Header;
