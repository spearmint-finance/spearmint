import sdk from "./sdk";
import type { Entity, EntityCreate, EntityUpdate } from "../types/entity";
import type {
  EntityCreate as SdkEntityCreate,
  EntityUpdate as SdkEntityUpdate,
} from "@spearmint-finance/sdk";
import { toSnakeCase, toCamelCase } from "../utils/caseConvert";

export const getEntities = async (): Promise<Entity[]> => {
  const response = await sdk.entities.listEntities();
  return toSnakeCase<Entity[]>(response.data);
};

export const getEntity = async (id: number): Promise<Entity> => {
  const response = await sdk.entities.getEntity(id);
  return toSnakeCase<Entity>(response.data);
};

export const createEntity = async (entity: EntityCreate): Promise<Entity> => {
  const body = toCamelCase<SdkEntityCreate>(entity);
  const response = await sdk.entities.createEntity(body);
  return toSnakeCase<Entity>(response.data);
};

export const updateEntity = async (
  id: number,
  entity: EntityUpdate
): Promise<Entity> => {
  const body = toCamelCase<SdkEntityUpdate>(entity);
  const response = await sdk.entities.updateEntity(id, body);
  return toSnakeCase<Entity>(response.data);
};

export const deleteEntity = async (id: number): Promise<void> => {
  await sdk.entities.deleteEntity(id);
};
