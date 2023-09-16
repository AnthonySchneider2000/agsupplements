import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IngredientItemInputComponent } from './ingredient-item-input.component';

describe('IngredientItemInputComponent', () => {
  let component: IngredientItemInputComponent;
  let fixture: ComponentFixture<IngredientItemInputComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [IngredientItemInputComponent]
    });
    fixture = TestBed.createComponent(IngredientItemInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
