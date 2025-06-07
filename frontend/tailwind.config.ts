import type { Config } from "tailwindcss";
const { heroui } = require("@heroui/react");

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@heroui/theme/dist/components/(button|form|input|modal|skeleton|ripple|spinner).js"
  ],
  theme: {
    extend: {
      fontFamily: {
        DanaLight: "DanaLight",
        DanaRegular: "DanaRegular",
        DanaMedium: "DanaMedium",
        DanaDemiBold: "DanaDemiBold",
      },
      colors: {
        secondary: "rgb(76 130 81)",
        primary: "#70db6f",
      },
      container:{
        
      }
    },
  },
  plugins: [heroui()],
} satisfies Config;
