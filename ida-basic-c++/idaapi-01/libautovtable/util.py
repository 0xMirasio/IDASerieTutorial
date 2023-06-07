import idaapi
import idautils
import idc
import idaapi
import ida_bytes
import ida_struct

INSN_SIZE = 8

def get_segrange_byname(segname):
    for ea in idautils.Segments():
        start,end = idc.get_segm_start(ea),idc.get_segm_end(ea) 
        name = idc.get_segm_name(start)
        if segname == name:
            return start,end
        
#in this implementation,every vtable start with a QWORD set to 0 then a offset to a reference of the vtable inside .rodata.rel.ro
def find_vtable(start, end):

    vtable_list = []
    for ea in idautils.Heads(start, end):
        
        #vtable start with a qword set to 0
        if idc.get_qword(ea) != 0:
            continue
        
        newea = ea + 8
        #check if next qword is a offset to a reference inside .rodata.rel.ro
        v = idc.get_qword(newea)
        if v == 0:
            continue
        
        if( v > end or v < start):
            continue
        
        newea += 8        

        vtable_size = 0
        while True:
            if idaapi.get_func(idc.get_qword(newea + vtable_size)) is None:
                break
                
            vtable_size += idaapi.get_item_size(newea + vtable_size)

        #on ne prend les vtables contenant 2 fonctions minimums
        if vtable_size >= 16:
        
            print("VTable found at address: {}".format(hex(ea)))
            vtable_list.append([ea, vtable_size])
            continue
            
    print("Done")
    return vtable_list

def populate_db(vtablelist):
    for vtable in vtablelist:
        
        vtable_name = f"vtable_{hex(vtable[0])}"
        print(f"Populating {vtable_name}")
        
        #delete old struct if exists
        existing_struct_id = ida_struct.get_struc_id(vtable_name)
        if existing_struct_id != idc.BADADDR:
            ida_struct.del_struc(existing_struct_id)
            
        vtable_struct_id = ida_struct.add_struc(idc.BADADDR, vtable_name)
        if vtable_struct_id == idc.BADADDR:
            print("Failed to create the structure!")
            return

        start_vtable = vtable[0] + 16
        for i in range(0, vtable[1] , INSN_SIZE): #CHANGE THIS TO 4 IF 32BIT PROGRAM
            v = idc.get_qword(start_vtable + i)
            name = f"sub_{hex(v)}"
            ida_struct.add_struc_member(ida_struct.get_struc(vtable_struct_id),name, i, ida_bytes.FF_QWORD | ida_bytes.FF_DATA, None, INSN_SIZE)
            
        print(f"Done creating {vtable_name}")
                    
    