import { useEffect, useState} from "react";
import "../pages/Proveedor.css";
const API_URL = "http://127.0.0.1:8000";

export default function Proveedor() {
  
  const [nombreProveedor, setNombreProveedor] = useState("");
  const [rtnProveedor, setRtnProveedor] = useState("");
  const [telefonos, setTelefonos] = useState([""]);
  const [nombreContacto, setNombreContacto] = useState("");
  const [correoElectronico, setCorreoElectronico] = useState("");
  const [activoProveedor, setActivoProveedor] = useState(true);

  const [paises, setPaises] = useState([]);
  const [paisProveedor, setPaisProveedor] = useState("");
  const [departamentos, setDepartamentos] = useState([]);
  const [departamentoProveedor, setDepartamentoProveedor] = useState("");
  const [ciudades, setCiudades] = useState([]);
  const [ciudadProveedor, setCiudadProveedor] = useState("");
  const [colonias, setColonias] = useState([]);
  const [coloniaProveedor, setColoniaProveedor] = useState("");
  const [calleProveedor, setCalleProveedor] = useState("");
  const [referenciasProveedor, setReferenciasProveedor] = useState("");

//Leer 
  const [proveedores, setProveedores] = useState([]);

  const [editandoId, setEditandoId] = useState(null);
  const [cargandoEdicion, setCargandoEdicion] = useState(false);
  const [eliminandoId, setEliminandoId] = useState(null);


  const [mensaje, setMensaje] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [enviando, setEnviando] = useState(false);

  //Paises
  useEffect(() => {
    async function cargarPaises() {
      try {
        const res = await fetch(`${API_URL}/ubicaciones/paises`);
        if (!res.ok) throw new Error("No se pudieron cargar los países");
        const data = await res.json();
        setPaises(data);
      } catch (err) {
        console.error(err);
      }
    }

    cargarPaises();
  }, []);

  //Departamentos
  useEffect(() => {
  if (!paisProveedor) return;

  let activo = true;

  async function cargarDepartamentos() {
    try {
      const res = await fetch(`${API_URL}/ubicaciones/departamentos/${paisProveedor}`);
      if (!res.ok) throw new Error("No se pudieron cargar los departamentos");
      const data = await res.json();
      if (activo) {
        setDepartamentos(data);
      }
    } catch (err) {
      if (activo) {
        console.error(err);
      }
    }
  }

  cargarDepartamentos();

  return () => {
    activo = false;
  };
}, [paisProveedor]);



//Ciudades
useEffect(() => {
  if(!departamentoProveedor) return;

  let activo = true;

  async function cargarCiudades(){
    try{
      const res = await fetch(`${API_URL}/ubicaciones/ciudades/${departamentoProveedor}`);
      if(!res.ok) throw new Error("No se pudieron cargar las Ciudades");
      const data = await res.json();
      if(activo){
        setCiudades(data);

      }
    } catch(err){
      if(activo){
        console.error(err);
      }
    }
  }
  cargarCiudades();
  return () => {
    activo = false;
  };
}, [departamentoProveedor]);


//Colonias
useEffect(() => {
  if(!ciudadProveedor) return;

  let activo = true;

  async function cargarColonias(){
    try{
      const res = await fetch(`${API_URL}/ubicaciones/direcciones/${ciudadProveedor}`);
      if(!res.ok) throw new Error("No se pudieron cargar las Colonias");
      const data = await res.json();
      if(activo){
        setColonias(data);
      }

    }catch(err){
      if(activo){
        console.error(err);
      }
    }

}    cargarColonias();
    return () => {
      activo = false;
};
}, [ciudadProveedor]);


//Telefonos

const TelefonoRegistro = (index, valor) => {
  const actualizados = [...telefonos];
  actualizados[index] = valor;

  if(index === actualizados.length - 1 && valor.trim() !== ""){
    actualizados.push("");
  }

  while(
    actualizados.length > 1 &&
    actualizados[actualizados.length - 1].trim() === "" &&
    actualizados[actualizados.length - 2].trim() === ""
  )
   {
    actualizados.pop();
   }
   setTelefonos(actualizados);
  };


  const guardarProveedor = async (e) => {
    e.preventDefault(); //previene que la pagina se recargue sola para evitar borrar datos
    setMensaje(""); //limpia mensajes de retroalimentacion
    setErrorMsg(""); 

    const telefonosFiltrados = telefonos
    .map((t) => t.trim())
    .filter((t) => t !== "");

    if(telefonosFiltrados.length === 0){
      setErrorMsg("Debes ingresar al menos un telefono");
      return;
    }

    const direccionSeleccionada = colonias.find(
      (c) => String(c.Id_Direccion) === String(coloniaProveedor)
    );

    if(!direccionSeleccionada){
      setErrorMsg("Debes seleccionar una colonia / direccion valida");
      return;
    }

    const calleTrim = calleProveedor.trim();
    const correoTrim = correoElectronico.trim();

    const datosProveedor = {
      direccion : {
        Id_Ciudad : Number(ciudadProveedor),
        colonia : direccionSeleccionada.colonia,
        calle : calleTrim === "" ? null : calleTrim,
        referencia : referenciasProveedor.trim(),
      },

      nombre_o_razonSocial: nombreProveedor.trim(),
      rtn: rtnProveedor.trim(),
      nombre_contacto: nombreContacto.trim(),
      correo: correoTrim === "" ? null : correoTrim,
      estado: activoProveedor ? 1 : 0,
      telefonos: telefonosFiltrados
    };

//Si se crea POST, si se edita PUT
    const esEdicion = editandoId !== null;
    const url = esEdicion
      ? `${API_URL}/proveedores/${editandoId}`
      : `${API_URL}/proveedores`;
    const metodo = esEdicion ? "PUT" : "POST";

    setEnviando(true);
    try {
      const res = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datosProveedor),
      });

      const data = await res.json();

      if (!res.ok) {
        const detalleTexto = Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(", ")
          : data.detail ||
            (esEdicion
              ? "No se pudo actualizar el proveedor"
              : "No se pudo registrar el proveedor");
        throw new Error(detalleTexto);
      }

      setMensaje(
        esEdicion
          ? `Proveedor "${data.nombre_o_razonSocial}" actualizado con exito`
          : `Proveedor "${data.nombre_o_razonSocial}" registrado con exito`
      );

      limpiarCamposProveedores();
      await cargarProveedores();
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setEnviando(false);
    }
    
  };


  //Listar Proveedores

    async function cargarProveedores(esActivo = ()  => true) {
    try {
      const res = await fetch(`${API_URL}/proveedores`);
      if(!res.ok) throw new Error("No se pudieron cargar los proveedores");
      const data = await res.json();
      if(esActivo()){
      setProveedores(data);
      }
    } catch(err) {
    if(esActivo()){
      console.error(err);
    }
    }
  }

  useEffect(() => {
    let activo = true;

    cargarProveedores(() => activo);

  return () => {
    activo = false;
  }

  }, []);

// Limpiar campos
function limpiarCamposProveedores(){
      setEditandoId(null);
      setNombreProveedor("");
      setRtnProveedor("");
      setTelefonos([""]);
      setNombreContacto("");
      setCorreoElectronico("");
      setPaisProveedor("");
      setDepartamentoProveedor("");
      setCiudadProveedor("");
      setColoniaProveedor("");
      setCalleProveedor("");
      setReferenciasProveedor("");
      setActivoProveedor(true);
      setDepartamentos([]);
      setCiudades([]);
      setColonias([]);
}

//formatear direccion
function formatearColoniaCalleReferencia(direccion) {
  if(!direccion) return "-"

  const colonia = direccion.colonia?.trim() || "";
  const calle = direccion.calle?.trim() || "";
  const referencia = direccion.referencia?.trim() || "";

  const parteColoniaCalle = calle ? `${colonia}, ${calle}` : colonia;

  if(parteColoniaCalle && referencia){
    return `${parteColoniaCalle} (${referencia})`;
  }
  return parteColoniaCalle || referencia || "-";
}


//Edicion
async function iniciarEdicion(prov){
    setMensaje("");
    setErrorMsg("");
    setCargandoEdicion(true);
    setEditandoId(prov.Id_Proveedor);

    setNombreProveedor(prov.nombre_o_razonSocial || "");
    setRtnProveedor(prov.rtn || "");
    setNombreContacto(prov.nombre_contacto || "");
    setCorreoElectronico(prov.correo || "");
    setActivoProveedor(prov.estado === 1);

    const nums =
    prov.telefonos && prov.telefonos.length > 0
    ? prov.telefonos.map((t) => t.telefono)
    : [""];

    //para mantener siempre la casilla extra al final
    setTelefonos([...nums, ""]);

    const dir = prov.direccion;
    setCalleProveedor(dir?.calle || "");
    setReferenciasProveedor(dir?.referencia || "");

    const ciudadObj = dir?.ciudad;
    const deptoObj = ciudadObj?.departamento;
    const paisObj = deptoObj?.pais;

    const idPais = paisObj?.Id_Pais ?? "";
    const idDepto = deptoObj?.Id_Departamento ?? ciudadObj?.Id_Departamento ?? "";
    const idCiudad = ciudadObj?.Id_Ciudad ?? dir?.Ciudad ?? "";

    try{
      setPaisProveedor(idPais ? String(idPais) : "");

      if(idPais) {
        const resDeptos = await fetch(`${API_URL}/ubicaciones/departamentos/${idPais}`);
        const dataDeptos = resDeptos.ok ? await resDeptos.json() : [];
        setDepartamentos(dataDeptos);
      } else {
        setDepartamentos([]);
      }

      setDepartamentoProveedor(idDepto ? String(idDepto) : "")

      if(idDepto) {
        const resCiudades = await fetch(`${API_URL}/ubicaciones/ciudades/${idDepto}`);
        const dataCiudades = resCiudades.ok ? await resCiudades.json() : [];
        setCiudades(dataCiudades);
      } else {
        setCiudades([]);
      }

      setCiudadProveedor(idCiudad ? String(idCiudad) : "");

      if (idCiudad) {
      const resColonias = await fetch(`${API_URL}/ubicaciones/direcciones/${idCiudad}`);
      const dataColonias = resColonias.ok ? await resColonias.json() : [];
      setColonias(dataColonias);

      // Para buscar si existe una colonia con el mismo nombre para preseleccionarla
      const encontrarColonia = dataColonias.find(
        (c) =>
          c.colonia?.trim().toLowerCase() ===
          dir?.colonia?.trim().toLowerCase()
      );
      setColoniaProveedor(encontrarColonia ? String(encontrarColonia.Id_Direccion) : "");
      } else {
        setColonias([]);
        setColoniaProveedor("");
      }

      } catch(err) {
        console.error(err);
        setErrorMsg("No se pudo cargar la ubicacion completa del proveedor");
      } finally {
        setCargandoEdicion(false);
      }
}

//Eliminar
async function EliminarProveedor(prov) {
  const confirmado = window.confirm(
    `¿Seguro que deseas eliminar permanentemente a "${prov.nombre_o_razonSocial}" (RTN: ${prov.rtn})? Esta acción no se puede deshacer.`
  );
  if (!confirmado) return;

  setMensaje("");
  setErrorMsg("");
  setEliminandoId(prov.Id_Proveedor);

  try {
    const res = await fetch(`${API_URL}/proveedores/${prov.Id_Proveedor}`, {
      method: "DELETE",
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "No se pudo eliminar el proveedor");
    }

    // Si estaba editando ese proveedor, limpia el formulario
    if (editandoId === prov.Id_Proveedor) {
      limpiarCamposProveedores();
    }

    setMensaje(`Proveedor "${prov.nombre_o_razonSocial}" eliminado con exito`);
    await cargarProveedores();
  } catch (err) {
    setErrorMsg(err.message);
  } finally {
    setEliminandoId(null);
  }
}


  return (
    <div className="proveedor-wrapper">
      <div className="proveedor-stack">
      <div className="proveedor-card">

            <div className="proveedor-header">
              <h1>Registro de Proveedores</h1>
              <p>Ingrese los datos del proveedor</p>
            </div>

              <form className="form-grid" onSubmit={guardarProveedor}>
                <div className="cards-dos-columnas">
                  <section className="sub-card">
                    <h2 className="sub-card-titulo">Datos del Proveedor</h2>

                <div className="form-prov">
                  <label htmlFor="n_rs-prov">* Nombre Completo o Razon Social</label>
                  <input
                    id="n_rs-prov"
                    type="text"
                    value={nombreProveedor}
                    onChange={(e) => setNombreProveedor(e.target.value)}
                    placeholder="Nombre del proveedor"
                    required
                  />
                </div>

                <div className="form-prov">
                  <label htmlFor="rtn-prov">* RTN</label>
                  <input
                    id="rtn-prov"
                    type="text"
                    value={rtnProveedor}
                    onChange={(e) => setRtnProveedor(e.target.value)}
                    placeholder="RTN del proveedor"
                    required
                  />
                </div>

                  <div className="form-prov">
                  <label htmlFor="n_contacto-prov">* Nombre de Contacto</label>
                  <input
                    id="n_contacto-prov"
                    type="text"
                    value={nombreContacto}
                    onChange={(e) => setNombreContacto(e.target.value)}
                    placeholder="Nombre del contacto"
                    required
                  />
                </div>

                  <div className="form-prov">
                  <label htmlFor="correo-prov">Correo Electrónico</label>
                  <input
                    id="correo-prov"
                    type="email"
                    value={correoElectronico}
                    onChange={(e) => setCorreoElectronico(e.target.value)}
                    placeholder="Proveedor@correo.com"
                  />
                </div>

                <div className="form-prov">
                    {telefonos.map((telefono, index) => ( 
                      <div key={index} className="telefono-item">
                  <label htmlFor={`telefono-prov-${index}`}>
                    {index === 0 ? "* Telefono" : `Telefono adicional ${index}`}
                    </label>
                  <input
                    id={`telefono-prov-${index}`}
                    type="text"
                    value={telefono}
                    onChange={(e) => TelefonoRegistro(index, e.target.value)}
                    placeholder={index === 0 ? "Telefono del proveedor" : "Otro telefono (opcional)"}
                    required={index === 0}
                  />
                </div>
                ))}
              </div>
      </section>


      <section className="sub-card">
      <h2 className="sub-card-titulo">Direccion</h2>

            <div className="form-prov">
            <label htmlFor="pais-prov">* Pais</label>
            <select
              id="pais-prov"
              value={paisProveedor}
              onChange={(e) => {
                const nuevoPais = e.target.value;
                setPaisProveedor(nuevoPais);
                setDepartamentoProveedor("");
                setCiudadProveedor("");
                setColoniaProveedor("");
                setDepartamentos([]);
                setCiudades([]);
                setColonias([]);
              }}
              required
            >
              <option value="">Seleccione un Pais</option>
              {paises.map((pais) => (
                <option key={pais.Id_Pais} value={pais.Id_Pais}>
                  {pais.nombre}
                </option>
              ))}
            </select>

          </div>

          <div className="form-prov">
            <label htmlFor="departamento-prov">* Departamento</label>
            <select
              id="departamento-prov"
              value={departamentoProveedor}
              onChange={(e) => {
                const nuevoDepartamento = e.target.value;
                setDepartamentoProveedor(nuevoDepartamento);
                setCiudadProveedor("");
                setColoniaProveedor("");
                setCiudades([]);
                setColonias([]);
                }}
                disabled={!paisProveedor}
              required
            >
              <option value="">Seleccione un Departamento</option>
              {departamentos.map((departamento) => (
                <option key={departamento.Id_Departamento} value={departamento.Id_Departamento}>
                  {departamento.nombre}
                </option>
              ))}
            </select>

          </div>

            <div className="form-prov">
            <label htmlFor="ciudad-prov">* Ciudad</label>
            <select
              id="ciudad-prov"
              value={ciudadProveedor}
              onChange={(e) => {
                const nuevaCiudad = e.target.value;
                setCiudadProveedor(nuevaCiudad);
                setColoniaProveedor("");
                setColonias([]);
              }}
              disabled={!departamentoProveedor}
              required
            >
              <option value="">Seleccione una Ciudad</option>
              {ciudades.map((ciudad) => (
                <option key={ciudad.Id_Ciudad} value={ciudad.Id_Ciudad}>
                  {ciudad.nombre}
                </option>
              ))}
            </select>

          </div>

          <div className="form-prov">
            <label htmlFor="colonia-prov">* Residencial - Colonia - Barrio</label>
            <select
              id="colonia-prov"
              value={coloniaProveedor}
              onChange={(e) => {
                const nuevaColonia = e.target.value;
                setColoniaProveedor(nuevaColonia);
              }}
              disabled={!ciudadProveedor}
              required
            >
              <option value="">Seleccione un residencial, colonia o barrio</option>
              {colonias.map((colonia) => (
                <option key={colonia.Id_Direccion} value={colonia.Id_Direccion}>
                  {colonia.colonia}
                </option>
              ))}
            </select>

          </div>

          <div className="form-prov">
                  <label htmlFor="calle-prov">Calle</label>
                  <input
                    id="calle-prov"
                    type="text"
                    value={calleProveedor}
                    onChange={(e) => setCalleProveedor(e.target.value)}
                    placeholder="Ej: Calle 1, etc."
                  />
                </div>

                        <div className="form-campo-completo">
                  <label htmlFor="referencias-prov">* Referencias</label>
                  <input
                    id="referencias-prov"
                    type="text"
                    value={referenciasProveedor}
                    onChange={(e) => setReferenciasProveedor(e.target.value)}
                    placeholder="Calle principal, contiguo a tiendas X, etc."
                    required
                  />
                </div>

                <div className="form-campo-completo checkbox-campo">
                <label htmlFor="activo-prov" className="checkbox-label">
                  <input
                    id="activo-prov"
                    type="checkbox"
                    checked={activoProveedor}
                    onChange={(e) => setActivoProveedor(e.target.checked)}
                  />
                  <span>Proveedor activo</span>
                </label>
              </div>

                </section>
            <button type="submit" disabled={enviando || cargandoEdicion} className="btn-primario" >
                Guardar Proveedor
            </button>
            {editandoId && (
              <button 
              type="button"
              disabled={enviando}
              className="btn-volver"
              onClick={limpiarCamposProveedores}
              >
                Cancelar Edicion
              </button>
            )}
            {errorMsg && <div className="mensaje-feedback">{errorMsg}</div>}
            {mensaje && <div className="mensaje-feedback">{mensaje}</div>}
            </div>


              </form>

            </div>

              <div className="proveedor-card tabla-proveedores-card">
                <div className="proveedor-header">
                  <h2>Proveedores Registrados</h2>
                  <p>Listado de proveedores en el sistema</p>
                </div>

                <div className="tabla-responsive">
                  <table className="tabla-proveedores">
                  <thead>
                          <tr>
                            <th>RTN</th>
                            <th>Nombre / Razón Social</th>
                            <th>Contacto</th>
                            <th>Correo</th>
                            <th>Teléfonos</th>
                            <th>Pais</th>
                            <th>Departamento / Ciudad</th>
                            <th>Colonia / Referencia</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                          </tr>
                        </thead>
                        <tbody>
                          {proveedores.length === 0 ? (
                            <tr>
                              <td colSpan="10" className="tabla-vacia">
                                No hay proveedores registrados aún.
                              </td>
                            </tr>
                          ) : (
                            proveedores.map((prov) => (
                              <tr key={prov.Id_Proveedor}>
                                <td>{prov.rtn}</td>
                                <td>{prov.nombre_o_razonSocial}</td>
                                <td>{prov.nombre_contacto}</td>
                                <td>{prov.correo || "—"}</td>
                                <td>
                                  {prov.telefonos && prov.telefonos.length > 0
                                    ? prov.telefonos.map((t) => t.telefono).join(", ")
                                    : "—"}
                                </td>
                                <td>{prov.direccion?.ciudad?.departamento?.pais?.nombre || "-"}</td>
                                <td>
                                  {prov.direccion?.ciudad
                                  ? `${prov.direccion.ciudad.departamento?.nombre || "-"}, ${prov.direccion.ciudad.nombre}`
                                    : "-"}
                                </td>
                                <td>
                                  {formatearColoniaCalleReferencia(prov.direccion)}
                                </td>
                                <td>
                                  <span
                                    className={`badge-estado ${
                                      prov.estado === 1 ? "activo" : "inactivo"
                                    }`}
                                  >
                                    {prov.estado === 1 ? "Activo" : "Inactivo"}
                                  </span>
                                </td>
                                <td>
                                  <div className="acciones-fila">
                                    <button
                                      type="button"
                                      className="btn-editar-fila"
                                      disabled={cargandoEdicion || eliminandoId === prov.Id_Proveedor}
                                      onClick={() => iniciarEdicion(prov)}
                                    >
                                      Editar
                                    </button>
                                    <button
                                      type="button"
                                      className="btn-eliminar-fila"
                                      disabled={eliminandoId === prov.Id_Proveedor}
                                      onClick={() => EliminarProveedor(prov)}
                                    >
                                      {eliminandoId === prov.Id_Proveedor ? "Eliminando..." : "Eliminar"}
                                    </button>
                                  </div>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                  </table>

                </div>



              </div>
    </div>

      </div>

      
      

  );
}