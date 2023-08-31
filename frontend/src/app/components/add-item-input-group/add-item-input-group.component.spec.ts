import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddItemInputGroupComponent } from './add-item-input-group.component';

describe('AddItemInputGroupComponent', () => {
  let component: AddItemInputGroupComponent;
  let fixture: ComponentFixture<AddItemInputGroupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddItemInputGroupComponent]
    });
    fixture = TestBed.createComponent(AddItemInputGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
