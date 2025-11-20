// Category types

export interface Category {
  id: number
  name: string
  parent_id?: number
  parent_name?: string
  description?: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface CategoryCreate {
  name: string
  parent_id?: number
  description?: string
  is_active?: boolean
}

export interface CategoryUpdate {
  name?: string
  parent_id?: number
  description?: string
  is_active?: boolean
}

