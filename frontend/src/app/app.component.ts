import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of, Subscription, timer } from "rxjs";
import { catchError, filter, switchMap } from "rxjs/operators";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  apiUrl = 'http://localhost:5000/getData'
  minutes!: number;
  subscription!: Subscription;
  intervalPeriod: number = 1;

  currencies: any;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.minutes = this.intervalPeriod * 60 * 1000;

    this.subscription = timer(0, this.minutes)
      .pipe(
        switchMap(() => {
          return this.getData()
            .pipe(catchError(err => {
              // Handle errors
              console.error(err);
              return of(undefined);
            }));
        }),
        filter(data => data !== undefined)
      )
      .subscribe(data => {
        this.currencies = data;
        console.log(this.currencies);
      });
  }
  getData() {
    return this.http.get(this.apiUrl);
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
