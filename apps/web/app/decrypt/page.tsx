"use client";

import axios from "axios";
import { useCallback, useEffect, useRef, useState } from "react";
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
import { ButtonGroup } from "@workspace/ui/components/button-group";
import { Input } from "@workspace/ui/components/input";
import { Button } from "@workspace/ui/components/button";
import { formatBytes } from "@/hooks/use-file-upload";
import type { State } from "@/components/FileSelector";
import FileSelector from "@/components/FileSelector";
import {
  IconCheck,
  IconClipboard,
  IconClock,
  IconCopy,
  IconDownload,
  IconFileInfo,
  IconKey,
  IconLoader,
  IconLockOpen2,
  IconReload,
  IconX,
} from "@tabler/icons-react";

type DownloadFile = {
  url: string;
  filename: string;
  size: number;
  label: string;
};

export default function Decrypt() {
  const [state, setState] = useState<State>("idle");
  const [formState, setFormState] = useState({
    file: null as File | null,
    decryptionMethod: null as string | null,
    decryptionKey: null as string | null,
  });
  const [downloadFiles, setDownloadFiles] = useState<DownloadFile[]>([]);
  const [timeTaken, setTimeTaken] = useState<number | null>(null);
  const [keyCopied, setKeyCopied] = useState(false);
  const clearFilesRef = useRef<(() => void) | null>(null);

  const playSound = () => {
    const audio = new Audio("/enchanting_table.ogg");
    audio.volume = 0.6;
    audio.play().catch(() => {});
  };

  useEffect(() => {
    console.log(formState.file);
  }, [formState.file]);

  const handleFileChange = useCallback((file: File | null) => {
    setFormState((prev) => ({ ...prev, file }));
  }, []);

  const handleSetClear = useCallback((clearFn: () => void) => {
    clearFilesRef.current = clearFn;
  }, []);

  const handleClear = useCallback(() => {
    downloadFiles.forEach((f) => window.URL.revokeObjectURL(f.url));
    if (clearFilesRef.current) {
      clearFilesRef.current();
    }
    setState("idle");
    setFormState({
      file: null,
      decryptionMethod: null,
      decryptionKey: null,
    });
    setDownloadFiles([]);
    setTimeTaken(null);
  }, [downloadFiles]);

  const handleDownload = (dlFile: DownloadFile) => {
    const link = document.createElement("a");
    link.href = dlFile.url;
    link.setAttribute("download", dlFile.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleDecrypt = async () => {
    playSound();

    const formData = new FormData();

    if (formState.file) {
      formData.append("file", formState.file);
    }
    if (formState.decryptionKey) {
      const key =
        formState.decryptionMethod === "hill"
          ? JSON.stringify({
              size: 2,
              matrix: JSON.parse(formState.decryptionKey),
            })
          : formState.decryptionKey;
      formData.append("key", key);
    }

    setState("processing");
    const startTime = performance.now();

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.post(
        `${apiUrl}/${formState.decryptionMethod}/decrypt`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response);

      const files: DownloadFile[] = [];
      const baseName = formState.file?.name.replace(/\.[^.]+$/, "") || "file";

      const decText = response.data.plaintext || "";
      const decTextBlob = new Blob([decText], { type: "text/plain" });
      files.push({
        url: window.URL.createObjectURL(decTextBlob),
        filename: `${baseName}_decrypted.txt`,
        size: decTextBlob.size,
        label: "Decrypted",
      });

      if (response.data.key !== undefined && response.data.key !== null) {
        const keyStr =
          typeof response.data.key === "object"
            ? JSON.stringify(response.data.key)
            : String(response.data.key);
        const keyBlob = new Blob([keyStr], { type: "text/plain" });
        files.push({
          url: window.URL.createObjectURL(keyBlob),
          filename: `${baseName}_key.txt`,
          size: keyBlob.size,
          label: "Key",
        });
      }

      setDownloadFiles(files);

      const endTime = performance.now();
      setTimeTaken((endTime - startTime) / 1000);

      setState("done");
    } catch (error) {
      console.error("Decryption error:", error);
      setState("error");
    }
  };

  return (
    <>
      <Header backButton titleText="Decrypt" />
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
              <FieldLabel htmlFor="input-button-group">
                Decryption Method
              </FieldLabel>
              <Select
                value={formState.decryptionMethod || ""}
                onValueChange={(value) =>
                  setFormState((prev) => ({ ...prev, decryptionMethod: value }))
                }
                disabled={state !== "idle"}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select decryption method" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectGroup>
                    <SelectItem value="caesar">Caesar Cipher</SelectItem>
                    <SelectItem value="permute">Permutation Cipher</SelectItem>
                    <SelectItem value="vigenere">Vigenère Cipher</SelectItem>
                    <SelectItem value="playfair">
                      Playfair Cipher (6x6)
                    </SelectItem>
                    <SelectItem value="hill">Hill Cipher (2x2)</SelectItem>
                    <SelectItem value="des">DES</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>

            <Field>
              <FieldLabel htmlFor="input-button-group">
                Decryption Key
              </FieldLabel>
              <ButtonGroup>
                <Input
                  id="input-button-group"
                  placeholder="Enter Key"
                  value={formState.decryptionKey || ""}
                  onChange={(e) =>
                    setFormState((prev) => ({
                      ...prev,
                      decryptionKey: e.target.value,
                    }))
                  }
                  disabled={state !== "idle"}
                />
                <Button
                  variant="outline"
                  className="leading-none"
                  disabled={state !== "idle"}
                  onClick={async () => {
                    const text = await navigator.clipboard.readText();
                    setFormState((prev) => ({ ...prev, decryptionKey: text }));
                  }}
                >
                  <IconClipboard className="size-4" aria-hidden="true" />
                  Paste Key
                </Button>
              </ButtonGroup>
            </Field>

            <Field className="grid grid-cols-5 mt-2">
              <Button
                className="col-span-3 w-full leading-none"
                disabled={
                  state !== "idle" ||
                  !formState.file ||
                  !formState.decryptionMethod ||
                  !formState.decryptionKey
                }
                onClick={handleDecrypt}
              >
                {state === "processing" ? (
                  <>
                    <IconLoader
                      className="size-4 animate-spin"
                      aria-hidden="true"
                    />
                    Decrypting...
                  </>
                ) : state === "done" ? (
                  <>
                    <IconCheck className="size-4" aria-hidden="true" />
                    Decrypted
                  </>
                ) : state === "error" ? (
                  <>
                    <IconX className="size-4" aria-hidden="true" />
                    Failed
                  </>
                ) : (
                  <>
                    <IconLockOpen2 className="size-4" aria-hidden="true" />{" "}
                    Decrypt
                  </>
                )}
              </Button>
              <Button
                className="col-span-2 w-full leading-none"
                variant="destructive"
                disabled={
                  state === "processing" ||
                  state === "done" ||
                  (formState.file === null &&
                    !formState.decryptionMethod &&
                    !formState.decryptionKey)
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
            <div className="flex flex-col justify-center items-start gap-4 text-sm text-muted-foreground w-full">
              <div className="flex flex-row flex-wrap justify-start items-center gap-1">
                <span className="flex justify-center items-center gap-1 leading-none">
                  <IconKey
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  Decryption Key:
                </span>
                <span className="flex justify-center items-center gap-1.5 leading-none">
                  {formState.decryptionKey}
                  <Button
                    size="icon-lg"
                    variant="ghost"
                    className="size-4"
                    onClick={() => {
                      navigator.clipboard.writeText(
                        formState.decryptionKey || ""
                      );
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
                <div key={dlFile.filename} className="flex items-center gap-1 leading-none">
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
                Decrypt Another File
              </Button>
            </div>
          </div>
        )}

        {state === "error" && (
          <div className="flex flex-col justify-between items-center gap-4 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <p className="text-red-400 dark:text-red-800">
              An error occurred during decryption. Please check your inputs and
              try again.
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
