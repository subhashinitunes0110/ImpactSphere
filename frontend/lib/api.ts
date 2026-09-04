const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function fetchFromAPI<T>(
  endpoint: string,
  fallbackData: T
): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      cache: "no-store",
    });

    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`);
    }

    return (await res.json()) as T;
  } catch (err) {
    console.warn(
      `Backend offline at ${endpoint}. Using fallback data.`,
      err
    );

    return fallbackData;
  }
}

export async function postToAPI<TRequest, TResponse>(
  endpoint: string,
  body: TRequest
): Promise<TResponse> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
    cache: "no-store",
  });

  if (!res.ok) {
    let message = `HTTP error ${res.status}`;

    try {
      const errorData = await res.json();

      if (typeof errorData?.detail === "string") {
        message = errorData.detail;
      } else {
        message = JSON.stringify(errorData);
      }
    } catch {
      // Keep default HTTP error message.
    }

    throw new Error(message);
  }

  return (await res.json()) as TResponse;
}