// utils/dayjs-jalali.ts
import dayjs from "dayjs";
import jalali from "jalali-dayjs";
import "dayjs/locale/fa";

dayjs.extend(jalali);
dayjs.locale("fa");

export function calenderConfig(weekOffset: number) {
  const weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه"];
  const today = dayjs();
  const dayOfWeek = today.day();
  const offsetToSaturday = (dayOfWeek + 1) % 7;
  const startOfWeek = today.subtract(offsetToSaturday, "day").add(weekOffset * 7, "day");

  const days = weekdays.map((_, i) => {
    const d = startOfWeek.add(i, "day");
    return {
      label: `${d.format("dddd")}، ${d.format("D MMMM YYYY")}`,
      key: d.format("YYYY-MM-DD"),
    };
  });

  const weekDateKey = startOfWeek.toISOString();

  return { days, weekDateKey };
}

export default dayjs;
