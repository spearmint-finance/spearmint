export interface Entity {
  entity_id: number;
  entity_name: string;
  entity_type: "personal" | "business" | "rental_property" | "side_hustle";
  tax_id?: string;
  address?: string;
  fiscal_year_start_month: number;
  is_default: boolean;
  notes?: string;
  account_count: number;
  created_at: string;
  updated_at: string;
}

export interface EntityCreate {
  entity_name: string;
  entity_type: "personal" | "business" | "rental_property" | "side_hustle";
  tax_id?: string;
  address?: string;
  fiscal_year_start_month?: number;
  is_default?: boolean;
  notes?: string;
}

export interface EntityUpdate {
  entity_name?: string;
  entity_type?: "personal" | "business" | "rental_property" | "side_hustle";
  tax_id?: string;
  address?: string;
  fiscal_year_start_month?: number;
  notes?: string;
}

export const ENTITY_TYPE_LABELS: Record<string, string> = {
  personal: "Personal",
  business: "Business",
  rental_property: "Rental Property",
  side_hustle: "Side Hustle",
};
