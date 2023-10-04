export interface Ingredient {
  id: number;
  name: string;
  description: string;
  price: number;
  units: string;
}

export interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
  link: string;
  servings: number;
  ingredients: ItemIngredient[];
  tags: string[];
}

export interface ItemIngredient {
  id: number;
  ingredient: Ingredient;
  mass: number;
}
