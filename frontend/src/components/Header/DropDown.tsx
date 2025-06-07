"use client";
import { logout } from "@/actions/auth";
import { Button, Dropdown, DropdownItem, DropdownMenu, DropdownTrigger } from "@heroui/react";
import { useRouter } from "next/navigation";
import React, { useActionState, useEffect } from "react";
import toast from "react-hot-toast";

function DropDown({ username, userid }: { username: string; userid: string | number }) {
  const [state, formAction, isPending] = useActionState(logout, { success: false });
  const router = useRouter();

  useEffect(() => {
    if (!isPending && state.success === true) {
      toast.success("با موفقیت خارج شدید!");

      setTimeout(() => {
        router.push("/login");
      }, 500);
    }
  }, [state, isPending]);
  return (
    <Dropdown>
      <DropdownTrigger>
        <div className="w-[40px] h-[40px] rounded-full flex items-center justify-center bg-white cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
          </svg>
        </div>
      </DropdownTrigger>
      <DropdownMenu aria-label="Dynamic Actions" className="bg-green-950 w-[300px] p-2 rounded-xl">
        <DropdownItem key={0}>
          <div className="flex items-center gap-3 pb-3 border-b border-b-white">
            <div className="w-[60px] h-[60px] rounded-full flex items-center justify-center bg-white cursor-pointer text-xl">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-7">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
              </svg>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-DanaMedium text-sm text-white">{username}</span>
              <span className="font-DanaMedium text-sm text-white">{userid}</span>
            </div>
          </div>
        </DropdownItem>
        <DropdownItem key={1}>
          <form action={formAction}>
            <Button type="submit" variant="solid" className="w-full font-DanaMedium bg-red-500 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
              </svg>
              خروج از سیستم
            </Button>
          </form>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
}

export default DropDown;
