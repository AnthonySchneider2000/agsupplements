import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {importProvidersFrom} from '@angular/core';
import {provideHttpClient} from '@angular/common/http';
import {provideAnimations} from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import {VERSION as MAT_VERSION, MatNativeDateModule} from '@angular/material/core';

import { AppComponent } from './app.component';
import { TestOutputComponent } from './components/test-output/test-output.component';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { IngredientItemInputComponent } from './components/ingredient-item-input/ingredient-item-input.component';
import { MatSelectModule } from '@angular/material/select';
import { IngredientItemTableComponent } from './components/ingredient-item-table/ingredient-item-table.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { TableOptionsComponent } from './components/table-options/table-options.component';
import { DynamicInfoTableComponent } from './components/dynamic-info-table/dynamic-info-table.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { DropzoneCdkModule } from '@ngx-dropzone/cdk';
import { DropzoneMaterialModule } from '@ngx-dropzone/material';


@NgModule({
  declarations: [
    AppComponent,
    TestOutputComponent,
    IngredientItemInputComponent,
    IngredientItemTableComponent,
    TableOptionsComponent,
    DynamicInfoTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSlideToggleModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatInputModule,
    MatButtonModule,
    FormsModule,
    MatSelectModule,
    MatCheckboxModule,
    MatFormFieldModule,
    DropzoneCdkModule,
    DropzoneMaterialModule,
  ],
  providers: [
    provideHttpClient(),
    provideAnimations(),
    importProvidersFrom(MatNativeDateModule),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
