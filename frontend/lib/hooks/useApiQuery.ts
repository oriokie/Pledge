import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';
import { APIError, handleAPIError } from '@/lib/utils/errorHandling';

interface QueryConfig<TData = unknown> {
  queryKey: unknown[];
  queryFn: () => Promise<TData>;
  options?: Omit<UseQueryOptions<TData, Error>, 'queryKey' | 'queryFn'>;
}

interface MutationConfig<T, V> extends Omit<UseMutationOptions<T, APIError, V>, 'mutationFn'> {
  mutationFn: (variables: V) => Promise<T>;
}

export function useApiQuery<TData = unknown>({ queryKey, queryFn, options }: QueryConfig<TData>) {
  return useQuery({
    queryKey,
    queryFn: async () => {
      try {
        return await queryFn();
      } catch (error) {
        handleAPIError(error);
        throw error;
      }
    },
    ...options,
  });
}

export function useApiMutation<T, V>({ mutationFn, ...options }: MutationConfig<T, V>) {
  return useMutation<T, APIError, V>({
    mutationFn: async (variables) => {
      try {
        return await mutationFn(variables);
      } catch (error) {
        throw handleAPIError(error);
      }
    },
    ...options,
  });
} 