import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AsyncTableComponent } from './async-table.component';

describe('AsyncTableComponent', () => {
  let component: AsyncTableComponent;
  let fixture: ComponentFixture<AsyncTableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AsyncTableComponent]
    });
    fixture = TestBed.createComponent(AsyncTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
