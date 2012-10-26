tinyMCE.init({
    mode: "exact",
    // theme: "advanced",
    // width:'800px',
    // height:'300px',    
    plugins: "spellchecker,directionality,paste,searchreplace",
    language: "{{ language }}",
    directionality: "{{ directionality }}",
    spellchecker_languages : "{{ spellchecker_languages }}",
    spellchecker_rpc_url : "{{ spellchecker_rpc_url }}"
});
