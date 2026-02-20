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
  IconClock,
  IconCopy,
  IconDice5,
  IconDownload,
  IconFileInfo,
  IconKey,
  IconLoader,
  IconLock,
  IconReload,
  IconX,
} from "@tabler/icons-react";

export default function Encrypt() {
  const [state, setState] = useState<State>("idle");
  const [formState, setFormState] = useState({
    file: null as File | null,
    encryptionMethod: null as string | null,
    encryptionKey: null as string | null,
  });
  const [encryptedFile, setEncryptedFile] = useState<{
    url: string;
    filename: string;
    size: number;
  } | null>(null);
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
    if (encryptedFile) {
      window.URL.revokeObjectURL(encryptedFile.url);
    }
    if (clearFilesRef.current) {
      clearFilesRef.current();
    }
    setState("idle");
    setFormState({
      file: null,
      encryptionMethod: null,
      encryptionKey: null,
    });
    setEncryptedFile(null);
    setTimeTaken(null);
  }, [encryptedFile]);

  const handleDownload = () => {
    if (!encryptedFile) return;

    const link = document.createElement("a");
    link.href = encryptedFile.url;
    link.setAttribute("download", encryptedFile.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleGenerateRandomKey = async () => {
    if (!formState.encryptionMethod) return;

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.get(
        `${apiUrl}/${formState.encryptionMethod}/key`
      );

      if (response.data) {
        const key =
          formState.encryptionMethod === "hill"
            ? JSON.stringify(response.data.matrix)
            : (response.data.key?.toString() ?? "");
        setFormState((prev) => ({
          ...prev,
          encryptionKey: key,
        }));
      }
    } catch (error) {
      console.error("Key generation error:", error);
    }
  };

  const handleEncrypt = async () => {
    playSound();

    const formData = new FormData();

    if (formState.file) {
      formData.append("file", formState.file);
    }
    if (formState.encryptionKey) {
      const key =
        formState.encryptionMethod === "hill"
          ? JSON.stringify({
              size: 2,
              matrix: JSON.parse(formState.encryptionKey),
            })
          : formState.encryptionKey;
      formData.append("key", key);
    }

    setState("processing");
    const startTime = performance.now();

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.post(
        `${apiUrl}/${formState.encryptionMethod}/encrypt`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        }
      );
      console.log(response);

      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);

      const contentDisposition = response.headers["content-disposition"];
      let filename = `encrypted_${formState.file?.name || "file"}`;
      if (contentDisposition) {
        filename = contentDisposition
          .split(";")[1]
          .split("=")[1]
          .replace(/"/g, "");
      }
      setEncryptedFile({ url, filename, size: blob.size });

      const endTime = performance.now();
      setTimeTaken((endTime - startTime) / 1000);

      setState("done");
    } catch (error) {
      console.error("Encryption error:", error);
      setState("error");
    }
  };

  return (
    <>
      <Header backButton titleText="Encrypt" />
      <main className="flex flex-col justify-center items-center gap-6 md:gap-10 p-4 md:p-6 w-full">
        <div className="flex flex-col md:flex-row justify-between items-center gap-10 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
          <FileSelector
            titleText="Add Plaintext File"
            setFile={handleFileChange}
            state={state}
            className="w-full"
            onClearFilesReady={handleSetClear}
          />
          <div className="flex flex-col justify-center items-center gap-6 md:gap-10 w-full">
            <Field>
              <FieldLabel htmlFor="input-button-group">
                Encryption Method
              </FieldLabel>
              <Select
                value={formState.encryptionMethod || ""}
                onValueChange={(value) =>
                  setFormState((prev) => ({ ...prev, encryptionMethod: value }))
                }
                disabled={state !== "idle"}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select encryption method" />
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
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>

            <Field>
              <FieldLabel htmlFor="input-button-group">
                Encryption Key
              </FieldLabel>
              <ButtonGroup>
                <Input
                  id="input-button-group"
                  placeholder="Enter Key"
                  value={formState.encryptionKey || ""}
                  onChange={(e) =>
                    setFormState((prev) => ({
                      ...prev,
                      encryptionKey: e.target.value,
                    }))
                  }
                  disabled={state !== "idle"}
                />
                <Button
                  variant="outline"
                  className="leading-none"
                  disabled={state !== "idle" || !formState.encryptionMethod}
                  onClick={handleGenerateRandomKey}
                >
                  <IconDice5 className="size-4" aria-hidden="true" />
                  Random
                </Button>
              </ButtonGroup>
            </Field>

            <Field className="grid grid-cols-5 mt-2">
              <Button
                className="col-span-3 w-full leading-none"
                disabled={
                  state !== "idle" ||
                  !formState.file ||
                  !formState.encryptionMethod ||
                  !formState.encryptionKey
                }
                onClick={handleEncrypt}
              >
                {state === "processing" ? (
                  <>
                    <IconLoader
                      className="size-4 animate-spin"
                      aria-hidden="true"
                    />
                    Encrypting...
                  </>
                ) : state === "done" ? (
                  <>
                    <IconCheck className="size-4" aria-hidden="true" />
                    Encrypted
                  </>
                ) : state === "error" ? (
                  <>
                    <IconX className="size-4" aria-hidden="true" />
                    Failed
                  </>
                ) : (
                  <>
                    <IconLock className="size-4" aria-hidden="true" /> Encrypt
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
                    !formState.encryptionMethod &&
                    !formState.encryptionKey)
                }
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Reset
              </Button>
            </Field>
          </div>
        </div>

        {state === "done" && (
          <div className="flex flex-col md:flex-row justify-between items-center gap-10 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <div className="flex flex-col justify-center items-start gap-4 text-sm text-muted-foreground w-full">
              {encryptedFile && (
                <div className="flex flex-row flex-wrap justify-start items-center gap-1">
                  <span className="flex justify-center items-center gap-1 leading-none">
                    <IconKey
                      className="size-4 inline-block"
                      aria-hidden="true"
                    />
                    Encryption Key:
                  </span>
                  <span className="flex justify-center items-center gap-1.5 leading-none">
                    {formState.encryptionKey}
                    <Button
                      size="icon-lg"
                      variant="ghost"
                      className="size-4"
                      onClick={() => {
                        navigator.clipboard.writeText(
                          formState.encryptionKey || ""
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

              {encryptedFile && (
                <div className="flex items-center gap-1 leading-none">
                  <IconFileInfo
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  File Size: {formatBytes(encryptedFile.size)}
                </div>
              )}
            </div>
            <div className="flex flex-col justify-center items-center gap-6 w-full">
              <Button
                className="w-full leading-none"
                variant="outline"
                onClick={handleDownload}
              >
                <IconDownload className="size-4" aria-hidden="true" />
                {encryptedFile?.filename || "N/A"}
              </Button>

              <Button
                className="text-red-500 hover:text-red-400 w-full leading-none"
                variant="outline"
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Encrypt Another File
              </Button>
            </div>
          </div>
        )}

        {state === "error" && (
          <div className="flex flex-col justify-between items-center gap-4 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <p className="text-red-400 dark:text-red-800">
              An error occurred during encryption. Please check your inputs and
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
