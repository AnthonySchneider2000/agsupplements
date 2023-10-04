import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './components/home-page/home-page.component';
import { ProductPageComponent } from './components/product-page/product-page.component';
import { CalculatorPageComponent } from './components/calculator-page/calculator-page.component';

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
