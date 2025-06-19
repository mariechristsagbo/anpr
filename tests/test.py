import asyncio
import cv2
from pathlib import Path
from fastanpr import FastANPR

async def process_image(anpr, image_path, output_dir):
    """Traite une seule image et sauvegarde les résultats."""
    print(f"\nTraitement de l'image: {image_path}")
    
    # Charger l'image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Erreur: Impossible de charger l'image {image_path}")
        return
    
    # Convertir de BGR à RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Détecter et reconnaître les plaques
    results = await anpr.run([image_rgb])
    
    # Afficher et traiter les résultats
    for plates in results:
        if not plates:
            print("  Aucune plaque détectée.")
            continue
            
        for plate in plates:
            # Debug : affiche les attributs disponibles
            print("Type :", type(plate))
            try:
                print("vars :", vars(plate))
            except Exception:
                print("dir :", dir(plate))
            
            # Récupère le texte de la plaque (prend ce qui existe)
            texte = getattr(plate, "rec_text", None) \
                or getattr(plate, "text", None) \
                or getattr(plate, "plate", None) \
                or getattr(plate, "number", None) \
                or str(plate)
            
            # Récupère la confiance
            conf = getattr(plate, "rec_conf", None) \
                or getattr(plate, "det_conf", None) \
                or getattr(plate, "conf", None)
            
            print(f"  Plaque détectée: {texte} (confiance: {conf})")
            
            # Dessiner la boîte englobante si elle existe
            box = getattr(plate, "det_box", None) or getattr(plate, "box", None)
            if box is not None and len(box) == 4:
                x1, y1, x2, y2 = box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"{texte} ({conf})", 
                            (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.9, (0, 255, 0), 2)
    
    # Créer le dossier de sortie s'il n'existe pas
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder l'image avec les résultats
    output_path = output_dir / f"result_{image_path.name}"
    cv2.imwrite(str(output_path), image)
    print(f"  Résultats sauvegardés dans: {output_path}")

async def main(input_dir, output_dir):
    # Initialiser le détecteur ANPR
    print("Initialisation du détecteur ANPR...")
    anpr = FastANPR(device="cuda")  # ou "cpu" si vous n'avez pas de GPU
    
    # Convertir les chemins en objets Path
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Lister toutes les images avec toutes les extensions courantes
    image_paths = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
        image_paths += list(input_dir.glob(ext))
    
    if not image_paths:
        print(f"Aucune image trouvée dans {input_dir}")
        return
    
    print(f"\nDébut du traitement de {len(image_paths)} images...")
    
    # Traiter chaque image
    for image_path in image_paths:
        await process_image(anpr, image_path, output_dir)
    
    print("\nTraitement terminé !")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Tester FastANPR sur des images personnalisées')
    parser.add_argument('--input', type=str, default='fastanpr/tests/images',
                        help='Dossier contenant les images à tester')
    parser.add_argument('--output', type=str, default='fastanpr/tests/results',
                        help='Dossier où sauvegarder les résultats')
    
    args = parser.parse_args()
    
    asyncio.run(main(args.input, args.output))
