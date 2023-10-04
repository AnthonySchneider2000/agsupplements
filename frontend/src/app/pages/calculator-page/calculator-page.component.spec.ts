import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalculatorPageComponent } from './calculator-page.component';

describe('CalculatorPageComponent', () => {
  let component: CalculatorPageComponent;
  let fixture: ComponentFixture<CalculatorPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CalculatorPageComponent]
    });
    fixture = TestBed.createComponent(CalculatorPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
