"use client";

import { useEffect } from "react";

export default function Figlet() {
  useEffect(() => {
    const figletText = ` ____    ______   ____    __  __  ____    ____       
/\\  _\`\\ /\\__  _\\ /\\  _\`\\ /\\ \\/\\ \\/\\  _\`\\ /\\  _\`\\     
\\ \\ \\/\\_\\/_/\\ \\/ \\ \\ \\L\\ \\ \\ \\_\\ \\ \\ \\L\\_\\ \\ \\L\\ \\   
 \\ \\ \\/_/_ \\ \\ \\  \\ \\ ,__/\\ \\  _  \\ \\  _\\L\\ \\ ,  /   
  \\ \\ \\L\\ \\ \\_\\ \\__\\ \\ \\/  \\ \\ \\ \\ \\ \\ \\L\\ \\ \\ \\\\ \\  
   \\ \\____/ /\\_____\\\\ \\_\\   \\ \\_\\ \\_\\ \\____/\\ \\_\\ \\_\\
    \\/___/  \\/_____/ \\/_/    \\/_/\\/_/\\/___/  \\/_/\\/ /`;

    console.log(
      `%c${figletText}\n`,
      "color: #5BAFE3; font-family: monospace; white-space: pre; line-height: normal;"
    );
  }, []);

  return null;
}
