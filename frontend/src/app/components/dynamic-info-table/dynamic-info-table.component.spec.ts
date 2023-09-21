import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DynamicInfoTableComponent } from './dynamic-info-table.component';

describe('DynamicInfoTableComponent', () => {
  let component: DynamicInfoTableComponent;
  let fixture: ComponentFixture<DynamicInfoTableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DynamicInfoTableComponent]
    });
    fixture = TestBed.createComponent(DynamicInfoTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
