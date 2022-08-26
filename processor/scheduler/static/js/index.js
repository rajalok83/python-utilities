function load_files(in_prnt_uid, in_prcs_uid, in_stts) {
  document.querySelector("#exampleModalLabel").innerHTML = in_prcs_uid;
  document.querySelector("#id_div_stts").innerHTML = in_stts;
  let list_id = ["id_div_gnrtd_fl", "id_div_lg_fl", "id_div_err_fl"];
  let list_extns = [".txt", ".log", ".err"];
  list_id.forEach((v, k) => {
    call_api("../load_files/" + in_prnt_uid + "/" + in_prcs_uid + list_extns[k], {}, "GET", function () {
      document.querySelector("#" + v).innerHTML = this.responseText;
    }, true, null);
  });
}

function run_template(id, nm, vndr_nm, prdct_typ, prdct_nm, prdct_vrsn, tmplt_txt) {
  edit_template(id, nm, vndr_nm, prdct_typ, prdct_nm, prdct_vrsn, tmplt_txt);
  document.querySelector("#editTemplateModalLabel").innerHTML = "Run Template";
  document.querySelector("#id_button_save").innerHTML = "Run";
  document.querySelectorAll("input, textarea").forEach(x => {
    x.setAttribute("disabled", "disabled");
  });
  document.querySelectorAll(".run-config").forEach(x => {
    x.style.display = '';
    x.setAttribute("required", "required");
  });
  document.querySelectorAll(".run-config-data").forEach(x => {
    x.removeAttribute("disabled");
  });

  call_api('../scheduler/connect_config/get?vndr_nm=' + vndr_nm + '&prdct_typ=' + prdct_typ + '&prdct_nm=' + prdct_nm + '&prdct_vrsn=' + prdct_vrsn, {}, 'GET', function () {
    let json_out = JSON.parse(this.responseText);
    document.querySelector("#id_input_cnnct_id").value = json_out["id"];
    document.querySelector("#id_input_cnnct_dir").value = json_out["cnnct_dir"];
    document.querySelector("#id_input_cnnct_strng").value = json_out["cnnct_strng"];
    document.querySelectorAll(".var").forEach(x => {
      x.remove();
    });
    let vars = json_out["cnnct_strng"].split("{{").map((x) => {
      console.log(x); if (x.includes(" }}")) {
        return x.split("}}")[0].trim();
      }
    }).filter((x) => x !== undefined && x != 'SCRPTFLPTH' && !"'\"".includes(x.substr(0, 1)));
    // console.log(vars);
    vars.reverse().forEach((in_var) => {
      console.log(document.querySelector("#id_div_form").innerHTML);
      let div = document.createElement('div');
      let div2 = document.createElement('div');
      div2.classList.add("input-group-prepared");
      div2.classList.add("run-config");
      div2.classList.add("var");
      let span = document.createElement('span');
      span.classList.add("input-group-text");
      span.innerText = in_var;
      div2.appendChild(span);
      let inpt = document.createElement('input');
      inpt.setAttribute("id", "id_input_" + in_var);
      inpt.setAttribute("name", "id_input_" + in_var);
      inpt.setAttribute("required", "required");
      inpt.classList.add("form-control");
      inpt.classList.add("run-config");
      inpt.classList.add("var");
      inpt.innerText = in_var;
      div.classList.add("input-group");
      div.classList.add("form-group");
      div.appendChild(div2);
      div.appendChild(inpt);
      document.querySelector("#id_div_form").appendChild(div);
    });
  }, true, null);
  document.querySelectorAll("button").forEach(x => {
    x.replaceWith(x.cloneNode(true));
  });
  document.querySelector("#id_button_save").addEventListener("click", on_run_template);
}

function on_run_template(e) {
  e.preventDefault();
  // const myModalAlternative = new bootstrap.Modal("#editTemplateModal", { backdrop: "static", keyboard: false });
  let form_data = new FormData(document.querySelector("#id_form"));
  form_data.append("tmplt_id", document.querySelector("#id_input_tmplt_id").value);
  form_data.append("cnnct_id", document.querySelector("#id_input_cnnct_id").value);
  call_api("../scheduler/run", form_data, "POST", function () {
    let json_out = JSON.parse(this.responseText);
    if (json_out["status"] == "failed") {
      alert("Failed with error " + json_out["text"])
    } else {
      console.log(json_out["text"]);
      if (json_out["text"]["pid"] !== undefined)
        location.href = location.protocol + "//" + location.hostname + (location.port == 80 ? "" : ":" + location.port) + "/scheduler/execution/" + json_out["text"]["pid"]
    }
  }, true, null);
}

function show_template(id) {
  document.querySelector("#editTemplateModal form").reset();
  document.querySelectorAll("button").forEach(x => {
    x.replaceWith(x.cloneNode(true));
  });
  document.querySelector("#editTemplateModalLabel").innerHTML = "Show Template";
  call_api("../template/get/" + id, null, "GET", function () {
    let json_out = JSON.parse(this.responseText);
    console.log(json_out);
    document.querySelector("#id_input_tmplt_id").value = json_out["id"];
    document.querySelector("#id_input_tmplt_nm").value = json_out["nm"];
    document.querySelector("#id_input_tmplt_vndr_nm").value = json_out["vndr_nm"];
    document.querySelector("#id_input_tmplt_prdct_typ").value = json_out["prdct_typ"];
    document.querySelector("#id_input_tmplt_prdct_nm").value = json_out["prdct_nm"];
    document.querySelector("#id_input_tmplt_prdct_vrsn").value = json_out["prdct_ver"];
    document.querySelector("#id_textarea_tmplt_txt").value = json_out["text"];
  })
}

function show_cnnct_config(id) {
  document.querySelector("#editConnectConfigModal form").reset();
  document.querySelectorAll("button").forEach(x => {
    x.replaceWith(x.cloneNode(true));
  });
  document.querySelector("#editConnectConfigModalLabel").innerHTML = "Show Connect Config";
  call_api("../scheduler/connect_config/get/" + id, null, "GET", function () {
    let json_out = JSON.parse(this.responseText);
    console.log(json_out);
    document.querySelector("#id_input_cnnct_id").value = json_out["id"];
    document.querySelector("#id_input_cnnct_vndr_nm").value = json_out["vndr_nm"];
    document.querySelector("#id_input_cnnct_prdct_typ").value = json_out["prdct_typ"];
    document.querySelector("#id_input_cnnct_prdct_nm").value = json_out["prdct_nm"];
    document.querySelector("#id_input_cnnct_prdct_vrsn").value = json_out["prdct_ver"];
    document.querySelector("#id_input_cnnct_dir").value = json_out["cnnct_dir"];
    document.querySelector("#id_input_cnnct_strng").value = json_out["cnnct_strng"];
  })
}

function edit_template(id, nm, vndr_nm, prdct_typ, prdct_nm, prdct_vrsn, tmplt_txt) {
  document.querySelector("#editTemplateModal form").reset();
  document.querySelectorAll("input, textarea").forEach(x => {
    x.removeAttribute("disabled");
  });
  document.querySelectorAll(".run-config").forEach(x => {
    x.style.display = 'none';
    x.removeAttribute("required");
  });
  document.querySelectorAll("button").forEach(x => {
    x.replaceWith(x.cloneNode(true));
  });
  if (id !== null) {
    document.querySelector("#editTemplateModalLabel").innerHTML = "Edit Template";
    document.querySelector("#id_input_tmplt_id").value = id;
    document.querySelector("#id_input_tmplt_nm").value = nm;
    document.querySelector("#id_input_tmplt_vndr_nm").value = vndr_nm;
    document.querySelector("#id_input_tmplt_prdct_typ").value = prdct_typ;
    document.querySelector("#id_input_tmplt_prdct_nm").value = prdct_nm;
    document.querySelector("#id_input_tmplt_prdct_vrsn").value = prdct_vrsn;
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
    document.querySelector("#id_input_cnnct_id").value = id;
    document.querySelector("#id_input_cnnct_vndr_nm").value = vndr_nm;
    document.querySelector("#id_input_cnnct_prdct_typ").value = prdct_typ;
    document.querySelector("#id_input_cnnct_prdct_nm").value = prdct_nm;
    document.querySelector("#id_input_cnnct_prdct_vrsn").value = prdct_vrsn;
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
  let id = document.querySelector("#id_input_cnnct_id").value;
  let vndr_nm = document.querySelector("#id_input_cnnct_vndr_nm").value;
  let prdct_typ = document.querySelector("#id_input_cnnct_prdct_typ").value;
  let prdct_nm = document.querySelector("#id_input_cnnct_prdct_nm").value;
  let prdct_vrsn = document.querySelector("#id_input_cnnct_prdct_vrsn").value;
  let cnnct_dir = document.querySelector("#id_input_cnnct_dir").value;
  let cnnct_strng = document.querySelector("#id_input_cnnct_strng").value;
  if (id !== "")
    call_api("./connect_config/update/" + id, { "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "cnnct_dir": cnnct_dir, "cnnct_strng": cnnct_strng }, "POST", function () { console.log(this.responseText); location.reload(); }, true, true);
  else
    call_api("./connect_config/create", { "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "cnnct_dir": cnnct_dir, "cnnct_strng": cnnct_strng }, "POST", function () { console.log(this.responseText); location.reload(); }, true, true);
}

function on_update_template(e) {
  e.preventDefault();
  let id = document.querySelector("#id_input_tmplt_id").value;
  let nm = document.querySelector("#id_input_tmplt_nm").value;
  let vndr_nm = document.querySelector("#id_input_tmplt_vndr_nm").value;
  let prdct_typ = document.querySelector("#id_input_tmplt_prdct_typ").value;
  let prdct_nm = document.querySelector("#id_input_tmplt_prdct_nm").value;
  let prdct_vrsn = document.querySelector("#id_input_tmplt_prdct_vrsn").value;
  let tmplt_txt = document.querySelector("#id_textarea_tmplt_txt").value;
  if (id !== "")
    call_api("./update/" + id, { "nm": nm, "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "tmplt_txt": tmplt_txt }, "POST", function () { console.log(this.responseText); location.reload(); }, true, true);
  else
    call_api("./create", { "nm": nm, "vndr_nm": vndr_nm, "prdct_typ": prdct_typ, "prdct_nm": prdct_nm, "prdct_vrsn": prdct_vrsn, "tmplt_txt": tmplt_txt }, "POST", function () { console.log(this.responseText); location.reload(); }, true, true);
}

function on_delete_template(e) {
  e.preventDefault();
  let id = document.querySelector("#id_confirm_input_id").value;
  console.log(id);
  if (id !== "")
    call_api("./delete/" + id, null, "POST", function () { console.log(this.responseText); location.reload(); }, true, null);
}

function delete_template(id, nm) {
  document.querySelector("#confirmTemplateModal form").reset();
  document.querySelector("#id_confirm_input_id").value = id;
  document.querySelector("#id_confirm_input_nm").value = nm;
  document.querySelector("#id_confirm_button_save").addEventListener("click", on_delete_template);
}

function delete_execution(id, nm) {
  document.querySelector("#confirmExecutionModal form").reset();
  document.querySelector("#id_confirm_input_id").value = id;
  document.querySelector("#id_confirm_input_nm").value = nm;
  document.querySelector("#id_confirm_button_save").addEventListener("click", on_delete_execution);
}

function on_delete_execution(e) {
  e.preventDefault();
  let id = document.querySelector("#id_confirm_input_id").value;
  if (id !== "")
    call_api("./execution/delete/" + id, null, "POST", function () { console.log(this.responseText); location.reload(); }, true, null);
}


function on_delete_connect_config(e) {
  e.preventDefault();
  let id = document.querySelector("#id_confirm_input_id").value;
  console.log(id);
  if (id !== "")
    call_api("./delete/" + id, null, "POST", function () { console.log(this.responseText); location.reload(); }, true, null);
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
function call_api(url, body, method, callback, isAsync, isMultiPart) {
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
  if (body !== null) {
    console.log(isMultiPart);
    if (isMultiPart != null)
      xhttp.send(JSON.stringify(body));
    else
      xhttp.send(body);
  }
  else
    xhttp.send();
}

function onbody_load() {
  document.querySelectorAll('.navbar-nav > li > a').forEach(x => {
    // console.log(x.href + " " + location.pathname);
    if (x.href === location.href)
      x.classList.add("active");
    else
      x.classList.remove("active");
    // console.log(location.protocol);
    // console.log(location.port);
    // console.log(x.href);
    // x.setAttribute("href", x.href);
  });
}

window.onload = onbody_load;