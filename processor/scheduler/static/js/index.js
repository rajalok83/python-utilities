function load_files(in_prnt_uid, in_prcs_uid, in_stts) {
  document.querySelector("#exampleModalLabel").innerHTML = in_prcs_uid;
  document.querySelector("#id_div_stts").innerHTML = in_stts;
  call_api("./load_files/" + in_prnt_uid + "/" + in_prcs_uid + ".txt", {}, "GET", function () {
    document.querySelector("#id_div_gnrtd_fl").innerHTML = this.responseText;
  }, true);
  call_api("./load_files/" + in_prnt_uid + "/" + in_prcs_uid + ".log", {}, "GET", function () {
    document.querySelector("#id_div_lg_fl").innerHTML = this.responseText;
  }, true);
  call_api("./load_files/" + in_prnt_uid + "/" + in_prcs_uid + ".err", {}, "GET", function () {
    document.querySelector("#id_div_err_fl").innerHTML = this.responseText;
  }, true);
}

function edit_template(id, nm, vndr_nm, prdct_typ, prdct_nm, prdct_vrsn, tmplt_txt) {
  document.querySelector("#editTemplateModal form").reset();
  if (id !== null) {
    document.querySelector("#editTemplateModalLabel").innerHTML = "Edit Template";
    document.querySelector("#id_input_id").value = id;
    document.querySelector("#id_input_nm").value = nm;
    document.querySelector("#id_input_vndr_nm").value = vndr_nm;
    document.querySelector("#id_input_prdct_typ").value = prdct_typ;
    document.querySelector("#id_input_prdct_nm").value = prdct_nm;
    document.querySelector("#id_input_prdct_vrsn").value = prdct_vrsn;
    document.querySelector("#id_textarea_tmplt_txt").value = tmplt_txt;
    document.querySelector("#id_button_save").innerHTML = "Update"
    document.querySelector("#id_button_save").addEventListener("click", on_update_template);
  }
  else {
    document.querySelector("#editTemplateModalLabel").innerHTML = "New Template";
    document.querySelector("#id_button_save").innerHTML = "Save";
    document.querySelector("#id_button_save").addEventListener("click", on_update_template);
  }
}

function edit_connect_config(id, vndr_nm, prdct_typ, prdct_nm, prdct_vrsn, cnnct_dir, cnnct_strng) {
  document.querySelector("#editConnectConfigModal form").reset();
  if (id !== null) {
    document.querySelector("#editConnectConfigModalLabel").innerHTML = "Edit Configuration";
    document.querySelector("#id_input_id").value = id;
    document.querySelector("#id_input_vndr_nm").value = vndr_nm;
    document.querySelector("#id_input_prdct_typ").value = prdct_typ;
    document.querySelector("#id_input_prdct_nm").value = prdct_nm;
    document.querySelector("#id_input_prdct_vrsn").value = prdct_vrsn;
    document.querySelector("#id_input_cnnct_dir").value = cnnct_dir;
    document.querySelector("#id_input_cnnct_strng").value = cnnct_strng;
    document.querySelector("#id_button_save").innerHTML = "Update"
    document.querySelector("#id_button_save").addEventListener("click", on_update_connect_config);
  }
  else {
    document.querySelector("#editConnectConfigModalLabel").innerHTML = "New Configuration";
    document.querySelector("#id_button_save").innerHTML = "Save";
    document.querySelector("#id_button_save").addEventListener("click", on_update_connect_config);
  }
}

function on_update_connect_config(e) {
  e.preventDefault();
  let id = document.querySelector("#id_input_id").value;
  let vndr_nm = document.querySelector("#id_input_vndr_nm").value;
  let prdct_typ = document.querySelector("#id_input_prdct_typ").value;
  let prdct_nm = document.querySelector("#id_input_prdct_nm").value;
  let prdct_vrsn = document.querySelector("#id_input_prdct_vrsn").value;
  let cnnct_dir = document.querySelector("#id_input_cnnct_dir").value;
  let cnnct_strng = document.querySelector("#id_input_cnnct_strng").value;
  if (id !== "")
    call_api("./update/" + id, { "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "cnnct_dir": cnnct_dir, "cnnct_strng": cnnct_strng }, "POST", function () { console.log(this.responseText); location.reload(); }, true);
  else
    call_api("./create", { "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "cnnct_dir": cnnct_dir, "cnnct_strng": cnnct_strng }, "POST", function () { console.log(this.responseText); location.reload(); }, true);
}

function on_update_template(e) {
  e.preventDefault();
  let id = document.querySelector("#id_input_id").value;
  let nm = document.querySelector("#id_input_nm").value;
  let vndr_nm = document.querySelector("#id_input_vndr_nm").value;
  let prdct_typ = document.querySelector("#id_input_prdct_typ").value;
  let prdct_nm = document.querySelector("#id_input_prdct_nm").value;
  let prdct_vrsn = document.querySelector("#id_input_prdct_vrsn").value;
  let tmplt_txt = document.querySelector("#id_textarea_tmplt_txt").value;
  if (id !== "")
    call_api("./update/" + id, { "nm": nm, "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "tmplt_txt": tmplt_txt }, "POST", function () { console.log(this.responseText); location.reload(); }, true);
  else
    call_api("./create", { "nm": nm, "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "tmplt_txt": tmplt_txt }, "POST", function () { console.log(this.responseText); location.reload(); }, true);
}

function on_delete_template(e) {
  e.preventDefault();
  let id = document.querySelector("#id_confirm_input_id").value;
  console.log(id);
  if (id !== "")
    call_api("./delete/" + id, null, "POST", function () { console.log(this.responseText); location.reload(); }, true);
}

function delete_template(id, nm) {
  document.querySelector("#confirmTemplateModal form").reset();
  document.querySelector("#id_confirm_input_id").value = id;
  document.querySelector("#id_confirm_input_nm").value = nm;
  document.querySelector("#id_confirm_button_save").addEventListener("click", on_delete_template);
}

function on_delete_connect_config(e) {
  e.preventDefault();
  let id = document.querySelector("#id_confirm_input_id").value;
  console.log(id);
  if (id !== "")
    call_api("./delete/" + id, null, "POST", function () { console.log(this.responseText); location.reload(); }, true);
}

function delete_connect_config(id, nm) {
  document.querySelector("#confirmConnectConfigModal form").reset();
  document.querySelector("#id_confirm_input_id").value = id;
  document.querySelector("#id_confirm_input_nm").value = nm;
  document.querySelector("#id_confirm_button_save").addEventListener("click", on_delete_connect_config);
}

function validate_template(in_tmpt_txt) {

  return true;
}
function call_api(url, body, method, callback, isAsync) {
  let xhttp = new XMLHttpRequest();
  if (callback !== undefined)
    xhttp.onload = callback;
  switch (method) {
    case "GET":
    case "POST":
    case "DELETE":
    case "UPDATE":
  }
  xhttp.open(method, url, isAsync);
  console.log(body);
  if (body !== null)
    xhttp.send(JSON.stringify(body));
  else
    xhttp.send();
}