$(document).ready(() => {
  $("#file-input").on("change", (event) => {
    const arquivos = event.target.files;
    if (!arquivos.length) {
      console.log("sem imagem pra mostrar");
      return;
    }
    const file = arquivos[0];
    if (!file.type.startsWith("image/")) {
      return alert("Formato não suportado");
    }
    // remove só a imagem dentro do #preview
    $("#preview img").remove();
    // cria a nova img e insere
    const img = $('<img class="img-fluid">').attr(
      "src",
      URL.createObjectURL(file)
    );
    $("#preview").prepend(img);
  });
});
