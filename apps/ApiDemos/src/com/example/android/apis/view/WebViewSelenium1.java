/*
 * Copyright (C) 2007 The Android Open Source Project
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package com.example.android.apis.view;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import com.example.android.apis.R;


/**
 * Webview to test Selenium web view interactions on android.
 */
public class WebViewSelenium1 extends Activity {
  public static final String HOME_PAGE_URL = "file:///android_asset/www/xhtmlTest.html";
  private WebView webView;

  @Override
  public void onCreate(Bundle icicle) {
    super.onCreate(icicle);

    setContentView(R.layout.webview_1);

    webView = (WebView) findViewById(R.id.wv1);
    webView.setWebViewClient(new ApiDemosWebViewClient());
  }

  @Override
  protected void onStart() {
    webView.loadUrl(HOME_PAGE_URL);
    super.onStart();
  }
  
  private class ApiDemosWebViewClient extends WebViewClient {
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, String url) {
      view.loadUrl(url);
      return true;
    }
  }
}
