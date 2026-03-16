import sdk from "./sdk";
import type { Entity, EntityCreate, EntityUpdate } from "../types/entity";

/**
 * Transform backend entity to frontend format.
 * Handles both camelCase (SDK) and snake_case (direct API) field names.
 */
const transformEntity = (raw: any): Entity => ({
  entity_id: raw.entityId ?? raw.entity_id,
  entity_name: raw.entityName ?? raw.entity_name,
  entity_type: raw.entityType ?? raw.entity_type,
  tax_id: raw.taxId ?? raw.tax_id,
  address: raw.address,
  fiscal_year_start_month:
    raw.fiscalYearStartMonth ?? raw.fiscal_year_start_month ?? 1,
  is_default: raw.isDefault ?? raw.is_default ?? false,
  notes: raw.notes,
  account_count: raw.accountCount ?? raw.account_count ?? 0,
  created_at: raw.createdAt ?? raw.created_at ?? "",
  updated_at: raw.updatedAt ?? raw.updated_at ?? "",
});

/** Base URL for direct API calls (SDK doesn't have entity endpoints yet). */
function getBaseUrl(): string {
  const sdkConfig = (sdk as any).config ?? {};
  return (
    sdkConfig.baseUrl ||
    sdkConfig.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined"
      ? window.location.origin
      : "http://localhost:8080")
  );
}

async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const url = `${getBaseUrl()}${path}`;
  const response = await fetch(url, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail || `API error: ${response.statusText}`);
  }
  if (response.status === 204 || options?.method === "DELETE") {
    return {} as T;
  }
  return response.json();
}

export const getEntities = async (): Promise<Entity[]> => {
  const data = await apiFetch<any[]>("/api/entities/");
  return data.map(transformEntity);
};

export const getEntity = async (id: number): Promise<Entity> => {
  const data = await apiFetch<any>(`/api/entities/${id}`);
  return transformEntity(data);
};

export const createEntity = async (entity: EntityCreate): Promise<Entity> => {
  const data = await apiFetch<any>("/api/entities/", {
    method: "POST",
    body: JSON.stringify({
      entity_name: entity.entity_name,
      entity_type: entity.entity_type,
      tax_id: entity.tax_id || null,
      address: entity.address || null,
      fiscal_year_start_month: entity.fiscal_year_start_month ?? 1,
      is_default: entity.is_default ?? false,
      notes: entity.notes || null,
    }),
  });
  return transformEntity(data);
};

export const updateEntity = async (
  id: number,
  entity: EntityUpdate
): Promise<Entity> => {
  const data = await apiFetch<any>(`/api/entities/${id}`, {
    method: "PUT",
    body: JSON.stringify(entity),
  });
  return transformEntity(data);
};

export const deleteEntity = async (id: number): Promise<void> => {
  await apiFetch<void>(`/api/entities/${id}`, { method: "DELETE" });
};
