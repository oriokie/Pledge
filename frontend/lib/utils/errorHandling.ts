export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export function handleAPIError(error: unknown): APIError {
  if (error instanceof APIError) {
    return error;
  }

  if (error instanceof Error) {
    return new APIError(error.message);
  }

  return new APIError('An unexpected error occurred');
}

export function isAPIError(error: unknown): error is APIError {
  return error instanceof APIError;
} 