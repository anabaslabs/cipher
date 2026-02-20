"use client";

import Link from "next/link";
import { IconBrandGithub } from "@tabler/icons-react";

export default function Footer() {
  function handleClink(url: string) {
    window.open(url, "_blank", "noopener,noreferrer");
  }

  return (
    <footer className="flex flex-col justify-center items-center gap-2 py-4 text-sm text-muted-foreground">
      <div className="flex justify-center items-center gap-1.5">
        <span>Built</span>
        <span>by</span>
        <a
          href="https://github.com/saptarshiroy39"
          target="_blank"
          rel="noopener noreferrer"
          className="underline hover:opacity-85"
        >
          Saptarshi Roy
        </a>
        <p
          className="underline hover:opacity-85 hover:cursor-pointer"
          onClick={() => handleClink("https://youtu.be/EA4DipdhpV8")}
        >
          &&
        </p>
        <a
          href="https://github.com/itskdhere"
          target="_blank"
          rel="noopener noreferrer"
          className="underline hover:opacity-85"
        >
          Krishnendu Das
        </a>
      </div>

      <Link
        href="https://github.com/anabaslabs/cipher"
        target="_blank"
        rel="noopener noreferrer"
        className="flex justify-center items-center gap-1 underline hover:opacity-85 leading-none"
      >
        <IconBrandGithub className="size-4" aria-label="GitHub Repository" />
        anabaslabs/cipher
      </Link>
    </footer>
  );
}
