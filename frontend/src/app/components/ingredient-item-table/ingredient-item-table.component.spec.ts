import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IngredientItemTableComponent } from './ingredient-item-table.component';

describe('IngredientItemTableComponent', () => {
  let component: IngredientItemTableComponent;
  let fixture: ComponentFixture<IngredientItemTableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [IngredientItemTableComponent]
    });
    fixture = TestBed.createComponent(IngredientItemTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
