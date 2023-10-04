import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { ProductPageComponent } from './pages/product-page/product-page.component';
import { CalculatorPageComponent } from './pages/calculator-page/calculator-page.component';

const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'product-page', component: ProductPageComponent },
  { path: 'calculator-page', component: CalculatorPageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
