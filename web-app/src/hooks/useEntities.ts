import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getEntities,
  createEntity,
  updateEntity,
  deleteEntity,
} from "../api/entities";
import type { EntityCreate, EntityUpdate } from "../types/entity";

export const useEntities = () => {
  return useQuery({
    queryKey: ["entities"],
    queryFn: getEntities,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCreateEntity = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: EntityCreate) => createEntity(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entities"] });
    },
  });
};

export const useUpdateEntity = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: EntityUpdate }) =>
      updateEntity(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entities"] });
    },
  });
};

export const useDeleteEntity = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteEntity(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entities"] });
    },
  });
};
