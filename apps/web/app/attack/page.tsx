"use client";

import axios from "axios";
import { useCallback, useRef, useState } from "react";
import Header from "@/components/Header";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select";
import { Field, FieldLabel } from "@workspace/ui/components/field";
import { Button } from "@workspace/ui/components/button";
import { Progress } from "@workspace/ui/components/progress";
import { formatBytes } from "@/hooks/use-file-upload";
import type { State } from "@/components/FileSelector";
import FileSelector from "@/components/FileSelector";
import {
  IconCheck,
  IconClock,
  IconCopy,
  IconDownload,
  IconFileInfo,
  IconKey,
  IconLoader,
  IconReload,
  IconSkull,
  IconX,
} from "@tabler/icons-react";

type DownloadFile = {
  url: string;
  filename: string;
  size: number;
  label: string;
};

export default function Attack() {
  const [state, setState] = useState<State>("idle");
  const [cipherMethod, setCipherMethod] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [downloadFiles, setDownloadFiles] = useState<DownloadFile[]>([]);
  const [guessedKey, setGuessedKey] = useState<string | null>(null);
  const [timeTaken, setTimeTaken] = useState<number | null>(null);
  const [keyCopied, setKeyCopied] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressStatus, setProgressStatus] = useState("");
  const clearFilesRef = useRef<(() => void) | null>(null);

  const playSound = () => {
    const audio = new Audio("/enchanting_table.ogg");
    audio.volume = 0.6;
    audio.play().catch(() => {});
  };

  const playCompleteSound = () => {
    const audio = new Audio("/challenge_complete.ogg");
    audio.volume = 0.2;
    audio.play().catch(() => {});
  };

  const handleFileChange = useCallback((f: File | null) => {
    setFile(f);
  }, []);

  const handleSetClear = useCallback((clearFn: () => void) => {
    clearFilesRef.current = clearFn;
  }, []);

  const handleClear = useCallback(() => {
    downloadFiles.forEach((f) => window.URL.revokeObjectURL(f.url));
    if (clearFilesRef.current) clearFilesRef.current();
    setState("idle");
    setCipherMethod(null);
    setFile(null);
    setDownloadFiles([]);
    setGuessedKey(null);
    setTimeTaken(null);
    setProgress(0);
    setProgressStatus("");
  }, [downloadFiles]);

  const handleAttack = async () => {
    if (!file || !cipherMethod) return;

    playSound();

    const formData = new FormData();
    formData.append("file", file);

    setState("processing");
    setProgress(0);
    setProgressStatus("Starting attack...");
    const startTime = performance.now();

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await fetch(
        `${apiUrl}/${cipherMethod}/attack/stream`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok || !response.body) {
        throw new Error("Stream failed");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let finalData: Record<string, unknown> | null = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const parsed = JSON.parse(line.slice(6));
              if (parsed.progress >= 0) {
                setProgress(parsed.progress);
              }
              if (parsed.status) {
                setProgressStatus(parsed.status);
              }
              if (parsed.result) {
                finalData = parsed.result;
              }
              if (parsed.error) {
                throw new Error(parsed.error);
              }
            } catch (parseErr) {
              if (parseErr instanceof Error && parseErr.message !== "Stream failed") {
              }
            }
          }
        }
      }

      if (!finalData) {
        throw new Error("No result received");
      }

      const data = finalData as { guessed_plaintext?: string; guessed_key?: unknown };
      const files: DownloadFile[] = [];
      const baseName = file.name.replace(/\.[^.]+$/, "");

      if (data.guessed_plaintext) {
        const blob = new Blob([data.guessed_plaintext], { type: "text/plain" });
        files.push({
          url: window.URL.createObjectURL(blob),
          filename: `${baseName}_Attacked.txt`,
          size: blob.size,
          label: "Attacked",
        });
      }
      if (data.guessed_key !== undefined && data.guessed_key !== null) {
        const keyStr =
          typeof data.guessed_key === "object" && (data.guessed_key as Record<string, unknown>).matrix
            ? JSON.stringify((data.guessed_key as Record<string, unknown>).matrix)
            : typeof data.guessed_key === "object"
              ? JSON.stringify(data.guessed_key)
              : String(data.guessed_key);
        const blob = new Blob([keyStr], {
          type: "text/plain",
        });
        files.push({
          url: window.URL.createObjectURL(blob),
          filename: `${baseName}_Key.txt`,
          size: blob.size,
          label: "Key",
        });
        setGuessedKey(keyStr);
      }

      setDownloadFiles(files);
      setTimeTaken((performance.now() - startTime) / 1000);
      setProgress(100);
      playCompleteSound();
      setState("done");
    } catch (error) {
      console.error("Attack error:", error);
      setState("error");
    }
  };

  const handleDownload = (dlFile: DownloadFile) => {
    const link = document.createElement("a");
    link.href = dlFile.url;
    link.setAttribute("download", dlFile.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <>
      <Header backButton titleText="Frequency Analysis Attack" />
      <main className="flex flex-col justify-center items-center gap-6 md:gap-10 p-4 md:p-6 w-full">
        <div className="flex flex-col md:flex-row justify-between items-center gap-10 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
          <FileSelector
            titleText="Add Ciphertext File"
            setFile={handleFileChange}
            state={state}
            className="w-full"
            onClearFilesReady={handleSetClear}
          />
          <div className="flex flex-col justify-center items-center gap-6 md:gap-10 w-full">
            <Field>
              <FieldLabel htmlFor="cipher-method-select">
                Cipher Method
              </FieldLabel>
              <Select
                value={cipherMethod || ""}
                onValueChange={setCipherMethod}
                disabled={state !== "idle"}
              >
                <SelectTrigger id="cipher-method-select" className="w-full">
                  <SelectValue placeholder="Select cipher method" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectGroup>
                    <SelectItem value="caesar">Caesar Cipher</SelectItem>
                    <SelectItem value="permute">Permutation Cipher</SelectItem>
                    <SelectItem value="vigenere">Vigenère Cipher</SelectItem>
                    <SelectItem value="hill">Hill Cipher (2x2)</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>

            {(state === "processing" || state === "done") && (
              <div className="flex flex-col gap-2 w-full">
                <div className="flex justify-between items-center text-xs text-muted-foreground">
                  <span>{progressStatus}</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            <Field className="grid grid-cols-5 mt-2">
              <Button
                className="col-span-3 w-full leading-none"
                disabled={state !== "idle" || !file || !cipherMethod}
                onClick={handleAttack}
              >
                {state === "processing" ? (
                  <>
                    <IconLoader
                      className="size-4 animate-spin"
                      aria-hidden="true"
                    />
                    Attacking...
                  </>
                ) : state === "done" ? (
                  <>
                    <IconCheck className="size-4" aria-hidden="true" />
                    Attacked
                  </>
                ) : state === "error" ? (
                  <>
                    <IconX className="size-4" aria-hidden="true" />
                    Failed
                  </>
                ) : (
                  <>
                    <IconSkull className="size-4" aria-hidden="true" />
                    Attack
                  </>
                )}
              </Button>
              <Button
                className="col-span-2 w-full leading-none"
                variant="destructive"
                disabled={
                  state === "processing" ||
                  state === "done" ||
                  (file === null && !cipherMethod)
                }
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Reset
              </Button>
            </Field>
          </div>
        </div>

        {state === "done" && downloadFiles.length > 0 && (
          <div className="flex flex-col md:flex-row justify-between items-center gap-10 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <div className="flex flex-col justify-center items-start gap-5 text-sm text-muted-foreground w-full">
              {guessedKey && (
                <div className="flex flex-row flex-wrap justify-start items-center gap-1">
                  <span className="flex justify-center items-center gap-1 leading-none">
                    <IconKey
                      className="size-4 inline-block"
                      aria-hidden="true"
                    />
                    Guessed Key:
                  </span>
                  <span className="flex justify-center items-center gap-1.5 leading-none">
                    {guessedKey}
                    <Button
                      size="icon-lg"
                      variant="ghost"
                      className="size-4"
                      onClick={() => {
                        navigator.clipboard.writeText(guessedKey || "");
                        setKeyCopied(true);
                        setTimeout(() => setKeyCopied(false), 2000);
                      }}
                      aria-label="Copy key to clipboard"
                    >
                      {keyCopied ? (
                        <IconCheck className="size-4" aria-hidden="true" />
                      ) : (
                        <IconCopy className="size-4" aria-hidden="true" />
                      )}
                    </Button>
                  </span>
                </div>
              )}

              {timeTaken !== null && (
                <div className="flex items-center gap-1 leading-none">
                  <IconClock
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  Time Taken: {timeTaken.toFixed(2)} seconds
                </div>
              )}

              {downloadFiles.map((dlFile) => (
                <div
                  key={dlFile.filename}
                  className="flex items-center gap-1 leading-none"
                >
                  <IconFileInfo
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  {dlFile.label} File Size: {formatBytes(dlFile.size)}
                </div>
              ))}
            </div>
            <div className="flex flex-col justify-center items-center gap-4 w-full">
              {downloadFiles.map((dlFile) => (
                <Button
                  key={dlFile.filename}
                  className="w-full leading-none"
                  variant="outline"
                  onClick={() => handleDownload(dlFile)}
                >
                  <IconDownload className="size-4" aria-hidden="true" />
                  {dlFile.filename}
                </Button>
              ))}

              <Button
                className="text-red-500 hover:text-red-400 w-full leading-none"
                variant="outline"
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Attack Another File
              </Button>
            </div>
          </div>
        )}

        {state === "error" && (
          <div className="flex flex-col justify-between items-center gap-4 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <p className="text-red-400 dark:text-red-800">
              An error occurred during the attack. Please check your file and
              cipher method and try again.
            </p>

            <Button
              className="w-full"
              variant="outline"
              onClick={() => setState("idle")}
            >
              Try Again
            </Button>
          </div>
        )}
      </main>
    </>
  );
}
