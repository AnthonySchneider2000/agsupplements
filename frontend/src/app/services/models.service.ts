export interface Ingredient {
  id: number;
  name: string;
  description: string;
  price: number;
  units: string;
}

export interface ItemWithIngredients {
  id: number;
  name: string;
  description: string;
  price: number;
  link: string;
  servings: number;
  ingredients: ItemIngredient[];
}

export interface ItemIngredient {
  id: number;
  ingredient: Ingredient;
  mass: number;
}
