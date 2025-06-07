"use client";
import { Button } from "@heroui/button";
import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import CalenderSkeleton from "./Skeleton";
import { groupFoodType } from "@/types/foods.type";
import Foods from "./Foods";
import { calenderConfig } from "@/utils/dayjs-jalali";

function Calender() {
  const [weekOffset, setWeekOffset] = useState(0);
  const { days, weekDateKey } = calenderConfig(weekOffset);
  const [groupedFoods, setGroupedFoods] = useState<groupFoodType>([]);

  const {
    data: foods,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["foods", weekOffset],
    queryFn: () => fetch(`/api/reserve?start-date=${weekDateKey}`).then((res) => res.json()),
    staleTime: 0,
  });

  useEffect(() => {
    if (!isLoading && foods?.data?.length && !isError) {
      const groupedData = foods.data.reduce((acc: any, item: any) => {
        acc[item.date] = acc[item.date] || [];
        acc[item.date].push(item);
        return acc;
      }, {});

      setGroupedFoods(Object.entries(groupedData) as []);
    }
  }, [isLoading, foods]);


  if (isError) {
    return <span className="font-DanaDemiBold text-lg text-red-500">متاسفانه خطایی رخ داده است!</span>;
  }

  return (
    <div className="flex flex-col mt-4 relative h-svh overflow-auto">
      <div className="sticky top-0 z-10 bg-white">
        <div className="w-full h-10 bg-primary rounded-md flex items-center justify-between overflow-hidden">
          <Button onPress={() => setWeekOffset((prev) => prev - 1)} className="flex items-center bg-primary transition-colors hover:bg-[#ffffff26] rounded-none">
            <span className="flex items-center justify-center bg-white size-7 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </span>
            <span className="font-DanaMedium text-white">هفته قبل</span>
          </Button>
          <span className="md:hidden text-white text-xs font-DanaRegular">{days[0].label}</span>
          <Button onPress={() => setWeekOffset((prev) => prev + 1)} className="flex items-center bg-primary transition-colors hover:bg-[#ffffff26] rounded-none">
            <span className="font-DanaMedium text-white">هفته بعد</span>
            <span className="flex items-center justify-center bg-white size-7 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
              </svg>
            </span>
          </Button>
        </div>
        <div className="hidden md:grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 h-[50px] items-center border-b border-b-black/15">
          {days.map((day) => (
            <span key={day.key} className="font-DanaMedium text-black/90 text-sm text-center">
              {day.label}
            </span>
          ))}
        </div>
      </div>
      {isLoading ? <CalenderSkeleton /> : !foods.data.length && !isLoading ? <div className="p-3 rounded-[10px] bg-[#fffbe6] border border-[#ffe58f] font-DanaMedium text-sm w-fit mx-auto mt-3">هیچ برنامه ی غذایی ای برای این تاریخ تعریف نشده است.</div> : <Foods groupedFoods={groupedFoods} weekOffset={weekOffset} />}
    </div>
  );
}

export default Calender;
