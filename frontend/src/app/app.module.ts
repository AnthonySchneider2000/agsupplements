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
import { TableComponent } from './components/table/table.component';
import { InputClearable } from './components/input-clearable/input-clearable.component';
import { TestOutputComponent } from './components/test-output/test-output.component';
import { AsyncTableComponent } from './components/async-table/async-table.component';
import { MatInputModule } from '@angular/material/input';


@NgModule({
  declarations: [
    AppComponent,
    TableComponent,
    TestOutputComponent,
    AsyncTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSlideToggleModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    InputClearable,
    MatInputModule,
  ],
  providers: [
    provideHttpClient(),
    provideAnimations(),
    importProvidersFrom(MatNativeDateModule),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }