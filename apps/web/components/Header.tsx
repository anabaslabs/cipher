"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { Button } from "@workspace/ui/components/button";
import { HyperText } from "@workspace/ui/components/hyper-text";
import { AnimatedThemeToggler } from "@workspace/ui/components/animated-theme-toggler";
import { IconArrowLeft } from "@tabler/icons-react";

export default function Header({
  titleText,
  backButton = false,
  animation = false,
}: {
  titleText?: string;
  backButton?: boolean;
  animation?: boolean;
}) {
  const router = useRouter();

  const playChestCloseSound = () => {
    const audio = new Audio("/chest_close.ogg");
    audio.volume = 0.2;
    audio.play().catch(() => {});
  };

  const handleBackClick = () => {
    playChestCloseSound();
    router.back();
  };

  return (
    <header className="flex justify-center items-center px-4 sm:px-6 py-4 w-full">
      <div className="flex justify-between items-center w-full max-w-6xl">
        <h1 className="flex justify-center items-center gap-2 text-2xl font-bold leading-none">
          {backButton ? (
            <Button
              size="icon"
              variant="secondary"
              className="rounded-full p-px"
              onClick={handleBackClick}
              aria-label="Go back"
            >
              <IconArrowLeft className="size-5" aria-hidden="true" />
            </Button>
          ) : (
            <Image src="/logo.png" alt="Cipher Logo" width={32} height={32} />
          )}
          {animation ? (
            <HyperText as="span">{titleText || "CIPHER"}</HyperText>
          ) : (
            <span>{titleText || "Cipher"}</span>
          )}
        </h1>
        <AnimatedThemeToggler className="p-1 border rounded-full bg-accent hover:bg-accent/70" />
      </div>
    </header>
  );
}
