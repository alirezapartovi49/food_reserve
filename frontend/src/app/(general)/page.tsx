// import Image from "next/image";
// import Link from "next/link";
// import React from "react";

// function page() {
//   return (
//     <section className="container xl:my-5 flex flex-wrap bg-primary xl:bg-white">
//       <div className="w-full xl:w-2/5 pt-5 xl:pt-0">
//         <div className="w-full xl:w-[400px] h-[200px] xl:h-[400px] rounded-2xl border-2 border-green-950 p-0 xl:p-[14px] bg-[#edf9ed] flex flex-col items-center justify-center">
//           {/* <Image src="./" alt="Food Empty Image"/> */}
//           <p className="mt-2 text-[#979797] font-DanaMedium">شما امروز غذای رزرو شده‌ای ندارید!</p>
//         </div>
//       </div>
//       <div className="w-full xl:w-3/5 mt-7 xl:mt-0 xl:p-7 xl:pl-0 border-t border-bt[#f8f8f8] xl:border-t-0 pt-7 xl:pt-0">
//         <div className="w-full grid grid-cols-3 xl:grid-cols-4 gap-2 xl:gap-0">
//           <Link href="/reserve" className="flex flex-col items-center justify-center gap-2 w-full xl:w-fit p-3 bg-[#f8f8f8] xl:bg-transparent rounded-lg xl:rounded-none">
//             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 54 54" className="w-11">
//               <path fill="#fff" stroke="#416447" strokeLinecap="round" strokeMiterlimit={10} strokeWidth={3} d="M27 52.389C41.022 52.389 52.39 41.022 52.39 27S41.022 1.611 27 1.611 1.611 12.978 1.611 27s11.367 25.389 25.39 25.389Z" />
//               <path fill="#fff" d="m31.179 51.783-1.025-16.018.084-.023a9.9 9.9 0 0 0 5.8-3.307c1.629-1.99-1.252-19.577-1.252-19.577" />
//               <path stroke="#17A52D" strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="m31.179 51.783-1.025-16.018.084-.023a9.9 9.9 0 0 0 5.8-3.307c1.629-1.99-1.252-19.577-1.252-19.577" />
//               <path fill="#fff" d="M19.805 12.864s-2.88 17.831-1.252 19.853a9.88 9.88 0 0 0 5.886 3.358l-.966 15.792" />
//               <path stroke="#17A52D" strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19.805 12.864s-2.88 17.831-1.252 19.853a9.88 9.88 0 0 0 5.886 3.358l-.966 15.792" />
//               <path stroke="#17A52D" strokeLinecap="round" strokeWidth={3} d="M27.297 29.59V12.86" />
//             </svg>
//             <span className="text-[#4c8251] font-DanaMedium text-sm">رزرو غذا</span>
//           </Link>
//           <Link href="/reserves-report" className="flex flex-col items-center justify-center gap-2 w-full xl:w-fit p-3 bg-[#f8f8f8] xl:bg-transparent rounded-lg xl:rounded-none">
//             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 60 43" className="w-11">
//               <g clipPath="url(#ic-reserve-report_svg__a)">
//                 <path fill="#fff" stroke="#416447" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" d="M56.938 1.468H3.062c-1.133 0-2.051 1.335-2.051 2.98v21.128c0 1.646.918 2.98 2.051 2.98h53.876c1.133 0 2.051-1.334 2.051-2.98V4.449c0-1.646-.918-2.98-2.051-2.98" />
//                 <path fill="#416447" d="M7.466 15.656v4.022h-1.53V9.198h2.106c.764-.085 1.526.188 2.176.778.24.281.43.643.553 1.054s.175.86.153 1.307a3.7 3.7 0 0 1-.35 1.646c-.253.502-.596.893-.992 1.129a479 479 0 0 0 2.121 4.566h-1.697l-1.722-4.022zm0-1.806h.493c.373.04.746-.082 1.07-.35.118-.127.21-.294.271-.487.06-.192.087-.404.076-.615a1.6 1.6 0 0 0-.076-.601 1.1 1.1 0 0 0-.277-.46 1.6 1.6 0 0 0-1.095-.315h-.464zM16.763 19.678h-4.155V9.198h4.155v1.82h-2.622v2.305h2.442v1.82h-2.442v2.703h2.625zM22.528 16.767c.012.428-.045.853-.167 1.242a2.8 2.8 0 0 1-.536.996c-.57.59-1.26.878-1.957.818-.705.02-1.405-.196-2.043-.632v-2.065q.6.405 1.236.667.454.184.927.194c.27.025.54-.073.772-.28a1 1 0 0 0 .208-.366 1.3 1.3 0 0 0 .061-.466 1.2 1.2 0 0 0-.118-.548 1.7 1.7 0 0 0-.348-.463 9 9 0 0 0-.936-.71 4.5 4.5 0 0 1-.991-.867 3.3 3.3 0 0 1-.528-.968 3.8 3.8 0 0 1-.198-1.29 3.8 3.8 0 0 1 .15-1.203c.113-.379.284-.715.5-.984.513-.568 1.149-.85 1.793-.795.362-.002.723.063 1.073.193q.55.213 1.069.545l-.494 1.729a6 6 0 0 0-.955-.481 2.2 2.2 0 0 0-.742-.136c-.24-.023-.477.081-.667.293a1 1 0 0 0-.175.346c-.04.133-.06.277-.056.422-.003.18.03.358.093.512q.12.257.3.422.469.41.969.735c.528.314 1.001.795 1.386 1.408.256.5.388 1.11.374 1.732M27.99 19.678h-4.154V9.198h4.155v1.82h-2.625v2.305h2.442v1.82h-2.442v2.703h2.625zM31.026 15.656v4.022h-1.53V9.198h2.106c.763-.085 1.526.188 2.176.778.24.281.43.643.553 1.054s.175.86.153 1.307a3.7 3.7 0 0 1-.35 1.646c-.253.502-.597.893-.993 1.129a488 488 0 0 0 2.123 4.566h-1.698l-1.723-4.022zm0-1.806h.494c.373.04.745-.082 1.07-.35a1.3 1.3 0 0 0 .27-.487c.06-.192.087-.404.076-.615a1.6 1.6 0 0 0-.076-.601 1.1 1.1 0 0 0-.277-.46 1.6 1.6 0 0 0-1.095-.315h-.463zM40.284 9.197h1.545l-2.453 10.481h-1.668L35.26 9.198h1.545l1.357 6.24q.114.55.235 1.285t.15 1.022q.134-1.17.37-2.308zM46.893 19.678h-4.156V9.198h4.156v1.82h-2.626v2.305h2.442v1.82h-2.442v2.703h2.626zM54.384 14.337a7.3 7.3 0 0 1-.213 2.14 5.8 5.8 0 0 1-.798 1.825c-.818.989-1.867 1.482-2.93 1.376h-2.042V9.198h2.265c1.002-.09 1.988.396 2.744 1.354a5.6 5.6 0 0 1 .763 1.743c.167.652.24 1.348.211 2.042m-1.59.058q0-3.377-2.052-3.377h-.814v6.825h.656q2.21 0 2.21-3.448" />
//                 <path fill="#6FDB6E" stroke="#416447" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" d="M33.34 25.143h-6.68v6.828h6.68z" />
//                 <path stroke="#416447" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" d="M30 31.971v9.56M20.148 41.532h19.703" />
//               </g>
//               <defs>
//                 <clipPath id="ic-reserve-report_svg__a">
//                   <path fill="#fff" d="M0 0h60v43H0z" />
//                 </clipPath>
//               </defs>
//             </svg>

//             <span className="text-[#4c8251] font-DanaMedium text-sm">وضعیت رزرو ها</span>
//           </Link>
//         </div>
//       </div>
//     </section>
//   );
// }

// export default page;




export const dynamic = "force-dynamic";
import Calender from "@/components/Reserver/Calender/Calender";

async function page() {
  return (
    <div className="container">
      <h1 className="text-xl font-DanaDemiBold mt-4">رزرو غذا</h1>
      <Calender />
    </div>
  );
}

export default page;
