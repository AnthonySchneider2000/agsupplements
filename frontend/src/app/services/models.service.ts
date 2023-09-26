export interface Ingredient {
  id: number;
  name: string;
  description: string;
  price: number;
}

export interface ItemWithIngredients {
  id: number;
  name: string;
  description: string;
  price: number;
  ingredients: ItemIngredient[];
  link: string;
}

export interface ItemIngredient {
  id: number;
  ingredient: Ingredient;
  mass: number;
}
