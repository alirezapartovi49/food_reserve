import { foodType, groupFoodType } from "@/types/foods.type";
import dayjs, { calenderConfig } from "@/utils/dayjs-jalali";
import { Button } from "@heroui/button";
import React, { useState } from "react";
import ReserveBtn from "./ReserveBtn";
import { Modal, ModalBody, ModalContent, ModalHeader, useDisclosure } from "@heroui/react";
import { useQRCode } from "next-qrcode";
import { useUser } from "@/contexts/auth";

function Foods({ groupedFoods, weekOffset }: { groupedFoods: groupFoodType; weekOffset: number }) {
  const { days } = calenderConfig(weekOffset);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [mainFood, setMainFood] = useState<foodType | null>(null);
  const user = useUser();
  const { Canvas } = useQRCode();
  const isUserReserved = user?.reserved_foods.filter((userFood) => userFood.food === mainFood?.id);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-5 gap-2 items-center p-2">
      <Modal isOpen={isOpen} size="lg" onClose={onClose} placement="center" className="!rounded-[10px] h-fit m-5">
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1 bg-primary !text-[#416447] font-DanaMedium text-base">جزئیات سفارش</ModalHeader>
              <ModalBody className="p-6 flex flex-col">
                <div className="w-full flex items-center justify-between">
                  <span className="text-[#4c8251] text-sm font-DanaDemiBold">ناهار</span>
                  <span className="text-sm text-[#706e6e] font-DanaDemiBold">{mainFood?.food_type === "pl" ? "15,000" : "10,000"} تومان</span>
                </div>
                {isUserReserved?.length ? (
                  <div className="flex flex-col items-center justify-center">
                    <Canvas
                      text={`${user?.id}${mainFood?.id}${user?.fullname}`}
                      options={{
                        errorCorrectionLevel: "M",
                        margin: 3,
                        scale: 4,
                        width: 150,
                        color: {
                          dark: "#000000",
                          light: "#ffffff",
                        },
                      }}
                    />
                    <span className="font-DanaRegular text-xs">
                      کد فراموشی: {user?.id}
                      {mainFood?.id}
                    </span>
                  </div>
                ) : (
                  ""
                )}

                <span className="font-DanaDemiBold text-base">{mainFood?.predefined_food?.name || mainFood?.custom_name}</span>
                <span className="font-DanaDemiBold text-base">کنار غذا: {mainFood?.side_fishes.map((sideDish, i) => (i === mainFood?.side_fishes.length - 1 ? sideDish.name : `${sideDish.name}, `))}</span>
              </ModalBody>
            </>
          )}
        </ModalContent>
      </Modal>
      {days.map((day, j) => (
        <div className="flex md:flex-col gap-2" key={day.key}>
          {groupedFoods
            .filter((group) => day.key === dayjs(dayjs(group[0]).toDate()).format("YYYY-MM-DD"))[0]?.[1][0]
            .foods.map((food: foodType, i: number) => (
              <div key={food.id} className={`flex flex-col w-full bg-[#f2f2f2] p-2.5 rounded-lg border-2 ${user?.reserved_foods?.find((userFood) => userFood.food === food.id) ? "border-secondary" : "border-transparent"}`}>
                <div className="w-full flex items-center justify-between">
                  <span className="text-[#4c8251] text-sm font-DanaDemiBold">ناهار</span>
                  <span className="text-sm text-[#706e6e] font-DanaMedium">{food.food_type === "pl" ? "15,000" : "10,000"} تومان</span>
                </div>
                <span className="text-center text-black/90 font-DanaDemiBold text-sm mt-4">{food.predefined_food?.name || food.custom_name}</span>
                <Button
                  onPress={() => {
                    setMainFood(food);
                    onOpen();
                  }}
                  className="text-[#ff9b36] text-xs font-DanaMedium bg-transparent mt-20 w-fit !h-8 !rounded-lg mx-auto"
                >
                  جزئیات غذا
                </Button>

                {groupedFoods[0]?.[1]?.[0]?.can_reserve ? <ReserveBtn groupedFoods={groupedFoods.find((gf) => gf[1][0].foods.some((f) => f.id == food.id)) as any} food={food} weekOffset={weekOffset} /> : ""}
              </div>
            ))}
        </div>
      ))}
    </div>
  );
}

export default Foods;
