import { Component, isDevMode } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

interface SearchResult {
  error?: string;
  path?: string[];
  ms?: number;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss',
})
export class SearchComponent {
  isLoading = false;
  result: SearchResult | null = null;

  form = new FormGroup({
    from: new FormControl(null, Validators.required),
    to: new FormControl(null, Validators.required),
  });

  async submit() {
    this.isLoading = true;
    this.result = null;

    const from = this.form.value.from;
    const to = this.form.value.to;

    const baseUrl = isDevMode() ? 'http://localhost:3000' : '/api';

    try {
      const res = await fetch(baseUrl + '/search?from=' + encodeURIComponent(from!) + '&to=' + encodeURIComponent(to!));

      const json = await res.json();
      const result = json as SearchResult;

      this.result = result;
    } catch (e: any) {
      console.log(e);
      this.result = { error: 'Service down!' };
    } finally {
      this.isLoading = false;
    }
  }
}
