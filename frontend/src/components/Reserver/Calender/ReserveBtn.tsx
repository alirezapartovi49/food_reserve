import { useUser } from "@/contexts/auth";
import { foodType, groupFoodType } from "@/types/foods.type";
import { Button } from "@heroui/button";
import { Spinner } from "@heroui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import React, { useState } from "react";
import toast from "react-hot-toast";

function ReserveBtn({ groupedFoods, food, weekOffset }: { groupedFoods: groupFoodType; food: foodType; weekOffset: number }) {
  const user = useUser();
  const isUserReserved = user?.reserved_foods.filter((userFood) => userFood.food === food.id);
  const [counter, setCounter] = useState(isUserReserved?.length as number);
  const queryClient = useQueryClient();

  const { mutate, isPending } = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/reserve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          date: groupedFoods?.[0],
          food: food.id,
        }),
      });

      if (res.status === 201) {
        return res;
      } else {
        throw new Error(`Server responded with status ${res.status}`);
      }
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["foods", weekOffset] });
      setCounter((prev) => prev + 1);
      toast.success("رزرو با موفقیت انجام شد!");
    },
    onError(res) {
      if (res.message.includes("400")) {
        toast.error("پر شدن حداکثر سقف مجاز!");
      } else if (res.message.includes("500")) {
        toast.error("خطا در برقراری ارتباط");
      } else {
        toast.error("خطایی رخ داده است");
      }
    },
  });

  return (
    <>
      {counter > 0 ? (
        <div className="p-1 shadow bg-white rounded-xl flex gap-1 w-2/3 mx-auto">
          <button className="bg-secondary flex items-center justify-center leading-8 text-white text-xl px-2 rounded-md h-8 w-9" onClick={() => mutate()}>
            {isPending ? <Spinner color="white" size="sm" /> : "+"}
          </button>
          <span className="flex-1 text-center px-2">{counter}</span>
          {/* <button className="bg-secondary flex items-center justify-center leading-8 text-white text-xl px-2 rounded-md" onClick={() => setCounter((prev) => (prev > 1 ? prev - 1 : 1))}>
            -
          </button> */}
        </div>
      ) : (
        <Button
          onPress={() => {
            mutate();
          }}
          className="text-white !bg-secondary w-fit !h-8 !rounded-lg mx-auto text-sm font-DanaMedium bg-transparent mt-2"
        >
          {isPending ? <Spinner size="sm" color="white" /> : "رزرو غذا"}
        </Button>
      )}
    </>
  );
}

export default ReserveBtn;
