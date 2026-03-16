import React, { createContext, useContext, useState, useCallback } from "react";
import type { Entity } from "../types/entity";
import { useEntities } from "../hooks/useEntities";

interface EntityContextValue {
  /** All available entities */
  entities: Entity[];
  /** Currently selected entity (null = "All Entities" view) */
  selectedEntity: Entity | null;
  /** Currently selected entity_id (null = all) */
  selectedEntityId: number | null;
  /** Select an entity by ID, or null for all */
  setSelectedEntityId: (id: number | null) => void;
  /** Whether entities are loading */
  isLoading: boolean;
}

const EntityContext = createContext<EntityContextValue>({
  entities: [],
  selectedEntity: null,
  selectedEntityId: null,
  setSelectedEntityId: () => {},
  isLoading: false,
});

export const EntityProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { data: entities = [], isLoading } = useEntities();
  const [selectedEntityId, setSelectedEntityIdState] = useState<number | null>(
    null
  );

  const setSelectedEntityId = useCallback(
    (id: number | null) => {
      setSelectedEntityIdState(id);
    },
    []
  );

  const selectedEntity =
    selectedEntityId != null
      ? entities.find((e) => e.entity_id === selectedEntityId) ?? null
      : null;

  return (
    <EntityContext.Provider
      value={{
        entities,
        selectedEntity,
        selectedEntityId,
        setSelectedEntityId,
        isLoading,
      }}
    >
      {children}
    </EntityContext.Provider>
  );
};

export const useEntityContext = () => useContext(EntityContext);
