import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DbManipInputGroupComponent } from './db-manip-input-group.component';

describe('DbManipInputGroupComponent', () => {
  let component: DbManipInputGroupComponent;
  let fixture: ComponentFixture<DbManipInputGroupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DbManipInputGroupComponent]
    });
    fixture = TestBed.createComponent(DbManipInputGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
