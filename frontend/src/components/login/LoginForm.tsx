"use client";
import { Form, Button, Input, Spinner } from "@heroui/react";
import React, { useEffect, useState, useTransition } from "react";
import { EyeFilledIcon, EyeSlashFilledIcon } from "../../../public/svgs";
import { useForm } from "react-hook-form";
import { login } from "@/actions/auth";
import toast from "react-hot-toast";
import { useRouter } from "next/navigation";

function LoginForm() {
  const [isVisible, setIsVisible] = React.useState(false);
  const toggleVisibility = () => setIsVisible(!isVisible);

  const router = useRouter();

  const [formState, setFormState] = useState({ error: undefined, success: false, status: null, data: null });
  const [isPending, startTransition] = useTransition();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append("email", data.email);
    formData.append("password", data.password);

    startTransition(async () => {
      const res = await login(null, formData);      
      setFormState(res as any);
    });
  };

  useEffect(() => {
    if (!isPending && formState?.status !== null) {
      if (formState?.success) {
        toast.success("ورود موفقیت‌آمیز بود!");
        setTimeout(() => {
          router.push("/");
        }, 500);
      } else {
        if (formState?.status === 401) {
          toast.error("نام کاربری یا رمز عبور اشتباه است!");
        } else if (formState?.status === 500) {
          toast.error("خطای ناشناخته رخ داده است");
        }
      }
    }
  }, [formState, isPending]);

  return (
    <Form validationBehavior="aria" onSubmit={handleSubmit(onSubmit)} autoComplete="on">
      <Input
        autoComplete="email"
        {...register("email", { required: "لطفا نام کاربری را وارد کنید" })}
        placeholder="نام کاربری"
        type="text"
        classNames={{
          inputWrapper: "bg-white hover:!bg-white !shadow-none transition-colors border border-[#d9d9d9] hover:!border-[#6a8f6c]",
        }}
        className="font-DanaMedium text-sm rounded-lg shadow-none"
      />
      {errors.email && <p className="text-red-500 text-sm mb-2 font-DanaMedium">{errors?.email?.message as string}</p>}

      <Input
        autoComplete="current-password"
        classNames={{
          inputWrapper: "bg-white hover:!bg-white !shadow-none transition-colors border border-[#d9d9d9] hover:!border-[#6a8f6c]",
        }}
        className="font-DanaMedium text-sm rounded-lg shadow-none"
        endContent={
          <button aria-label="toggle password visibility" className="focus:outline-none" type="button" onClick={toggleVisibility}>
            {isVisible ? <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" /> : <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />}
          </button>
        }
        {...register("password", {
          required: "لطفا رمز عبور را وارد کنید",
          minLength: {
            value: 8,
            message: "رمز عبور باید حداقل ۸ کاراکتر باشد",
          },
        })}
        placeholder="رمز عبور"
        type={isVisible ? "text" : "password"}
        variant="bordered"
      />
      {errors.password && <p className="text-red-500 text-sm mb-2 font-DanaMedium">{errors?.password?.message as string}</p>}

      <Button type="submit" className={`w-full font-DanaMedium text-sm rounded-lg !bg-[#ffb142] text-white ${isPending ? "opacity-70" : "opacity-100"}`} disabled={isPending}>
        {isPending ? <Spinner color="white" size="sm" /> : "ورود"}
      </Button>
    </Form>
  );
}

export default LoginForm;
